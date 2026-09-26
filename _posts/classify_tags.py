#!/usr/bin/env python3
"""Classify Jekyll posts into tags with OpenRouter's Jev Decisions API.

Examples:
  export OPENROUTER_API_KEY="..."
  python _posts/classify_tags.py                 # preview suggested tags
  python _posts/classify_tags.py --write         # update front matter
  python _posts/classify_tags.py --file 2026-09-26-a-personal-canon-of-biology-essays.md --write

The script never sends the API key anywhere except OpenRouter. It strips post
front matter before classification so existing tags do not influence the result.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = "typesafe/jev-1.13"
POSTS_DIR = Path(__file__).resolve().parent

TAG_CRITERIA = {
    "writing": "A reflective, personal, cultural, or general essay about ideas or craft.",
    "ai": "Substantively about artificial intelligence, machine learning, or language models.",
    "science": "Substantively about scientific research, scientific reasoning, chemistry, biology, or medicine.",
    "life": "Substantively about life experience, habits, relationships, wellbeing, or personal development.",
    "coding": "Substantively about programming, software engineering, tools, or technical implementation.",
    "agents": "Substantively about AI agents, agentic systems, tool use, or autonomous workflows.",
    "automation": "Substantively about automating tasks or processes, laboratory robotics, instrument coordination, or reducing manual work through software and hardware.",
    "travel": "Substantively about travel, places, or a trip.",
    "papers": "Primarily discusses, reviews, recommends, or closely analyzes academic papers or research literature.",
}

FRONT_MATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
# Matches both `tags: [ai, science]` and the older YAML-list form:
# tags:\n# - AI
TAGS_LINE = re.compile(r"^tags:[^\n]*(?:\n[ \t]*-\s+[^\n]+)*", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Suggest or write Jev-generated tags for Jekyll posts.")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        metavar="POST",
        help="A post filename in _posts. May be given more than once. Defaults to all Markdown posts.",
    )
    parser.add_argument("--write", action="store_true", help="Write suggested tags into YAML front matter.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.75,
        help="Minimum include probability required for a tag (default: 0.75)."
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=14000,
        help="Maximum post-body characters sent to the API (default: 14000).",
    )
    return parser.parse_args()


def post_paths(filenames: list[str]) -> list[Path]:
    if not filenames:
        return sorted(path for path in POSTS_DIR.glob("*.md") if path.is_file())

    paths = []
    for filename in filenames:
        path = POSTS_DIR / filename
        if not path.is_file() or path.suffix != ".md":
            raise ValueError(f"Post not found in {POSTS_DIR}: {filename}")
        paths.append(path)
    return paths


def body_without_front_matter(text: str) -> str:
    return FRONT_MATTER.sub("", text, count=1).strip()


def questions() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for tag, criterion in TAG_CRITERIA.items():
        result[f"tag_{tag}"] = {
            "type": "choice",
            "instructions": f"Should this post receive the '{tag}' tag? Judge the post's central subject, not a passing mention.",
            "criteria": {
                "include": criterion,
                "exclude": f"The post is not centrally about this category ({tag}).",
            },
        }
    return result


def classify(body: str, api_key: str) -> dict[str, Any]:
    request = Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://www.pushkarghanekar.com",
            "X-OpenRouter-Title": "Pushkar Ghanekar blog tagger",
        },
        data=json.dumps({"model": MODEL, "state": body, "questions": questions()}).encode("utf-8"),
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"OpenRouter returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach OpenRouter: {error.reason}") from error

    if "answers" not in payload:
        raise RuntimeError(f"Unexpected API response: {json.dumps(payload)[:500]}")
    return payload["answers"]


def include_probability(answer: dict[str, Any]) -> float:
    probabilities = answer.get("probabilities", {})
    if isinstance(probabilities, dict):
        return float(probabilities.get("include", 0.0))
    # Be defensive if the API returns a list of {choice, probability} objects.
    if isinstance(probabilities, list):
        for item in probabilities:
            if item.get("choice") == "include":
                return float(item.get("probability", 0.0))
    return 1.0 if answer.get("choice") == "include" else 0.0


def suggested_tags(answers: dict[str, Any], threshold: float) -> list[tuple[str, float]]:
    tags = []
    for tag in TAG_CRITERIA:
        answer = answers.get(f"tag_{tag}", {})
        probability = include_probability(answer)
        if answer.get("choice") == "include" and probability >= threshold:
            tags.append((tag, probability))
    return tags


def write_tags(path: Path, text: str, tags: list[str]) -> None:
    if not text.startswith("---\n"):
        raise ValueError(f"{path.name} has no YAML front matter; refusing to edit it.")

    front_matter_match = FRONT_MATTER.match(text)
    if not front_matter_match:
        raise ValueError(f"{path.name} has malformed YAML front matter; refusing to edit it.")

    front_matter = front_matter_match.group(0)
    tag_line = "tags: [" + ", ".join(tags) + "]"
    if TAGS_LINE.search(front_matter):
        replacement = TAGS_LINE.sub(tag_line, front_matter)
    else:
        replacement = front_matter[:-4] + tag_line + "\n---\n"
    path.write_text(replacement + text[front_matter_match.end() :])


def main() -> int:
    args = parse_args()
    if not 0.0 <= args.threshold <= 1.0:
        raise ValueError("--threshold must be between 0 and 1.")

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY is required. Example: export OPENROUTER_API_KEY='...'")
        return 2

    paths = post_paths(args.file)
    for path in paths:
        text = path.read_text()
        body = body_without_front_matter(text)
        if len(body) > args.max_chars:
            body = body[: args.max_chars] + "\n\n[Post truncated for classification.]"

        answers = classify(body, api_key)
        tags_with_confidence = suggested_tags(answers, args.threshold)
        tags = [tag for tag, _ in tags_with_confidence]
        confidence = ", ".join(f"{tag} ({score:.0%})" for tag, score in tags_with_confidence) or "no tags"
        print(f"{path.name}: {confidence}")

        if args.write:
            write_tags(path, text, tags)

    if not args.write:
        print("\nPreview only. Re-run with --write to update post front matter.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
