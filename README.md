# Pushkar Ghanekar

A small, Markdown-first personal site built with [Jekyll](https://jekyllrb.com/).

## Design direction

Design direction: a quiet, personal, writing-first presentation:

- A narrow introduction with a small portrait and generous, stable top spacing. Opening a disclosure never recenters the page.
- Navigation below the write-up, followed by four small social icons.
- System sans-serif body text, restrained serif headings, and readable serif essays.
- Light and dark palettes, no external fonts or UI frameworks. Brief CSS reveals and quiet hover transitions respect reduced-motion preferences; no looping animation or scroll interception.
- One shared layout, one plain CSS file, and a small theme script. Everything except the theme toggle works without JavaScript.

Keep new features subordinate to the writing. Avoid hero banners, cards, rotating images, and extra navigation bars.

## Writing a post

Add a Markdown file to `_posts` named `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: A useful title
date: 2025-01-01
description: A short optional summary.
tags: [Writing, Science]
---

Write in Markdown.
```

Posts automatically appear at `/blog/`, in the tag index, and in the RSS feed at `/feed.xml`.

## Local development

Requires Ruby and Bundler:

```sh
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000`. Build the production site with `bundle exec jekyll build`.

## Structure

- `index.html` — personal landing page with collapsible life updates and principles (`landing: true`)
- `about.md` — extended biography at `/about/`
- `blog.md` — writing index at `/blog/`
- `publications.md` — publications and Scholar link
- `tags.html` — tag index and archives
- `_posts/` — Markdown posts, with existing URLs preserved
- `_layouts/default.html` — shared document, theme control, and footer
- `_layouts/post.html` — article header and reading layout
- `_includes/` — shared navigation and social icons
- `assets/css/main.css` — plain CSS, no preprocessing
- `assets/js/theme.js` — saved theme preference; falls back safely when storage is blocked
- `assets/pdf/June2024_Pushkar_CV.pdf` — the directly linked CV (June 2024 version)

Social URLs live in `_config.yml`; page links live in `_includes/navigation.html`. Restart Jekyll after changing `_config.yml`.

## Domain email forwarding

Incoming email uses **ImprovMX**, with DNS managed by **Netlify DNS**. Forwarding was configured and delivery to Gmail confirmed on September 26, 2026.

```text
Visitor → hello@pushkarghanekar.com → ImprovMX → private Gmail inbox
```

The Gmail destination is stored only in the ImprovMX dashboard. Do not put it, account credentials, or API keys in this repository or public DNS records. Visitors see only the public `hello@pushkarghanekar.com` address.

### Configuration

1. In [ImprovMX](https://improvmx.com/), add `pushkarghanekar.com` (without `www`).
2. Create the `hello` alias and set the private Gmail inbox as its forwarding destination. Complete any destination verification requested.
3. In Netlify, open the domain's **Netlify DNS → DNS records** and add the records below. Use the root domain (`pushkarghanekar.com`, or `@` if the interface accepts it), not `www`.

| Type | Name | Priority | Value |
| --- | --- | --- | --- |
| MX | `pushkarghanekar.com` | 10 | `mx1.improvmx.com` |
| MX | `pushkarghanekar.com` | 20 | `mx2.improvmx.com` |
| TXT | `pushkarghanekar.com` | — | `v=spf1 include:spf.improvmx.com ~all` |

Leave TTL at the provider default. These are the records verified at setup; consult ImprovMX's current instructions if recreating the service. Keep existing website DNS records, nameservers, and HTTPS settings unchanged. Email forwarding does not require a website deployment or a contact form.

If other email services are added later, combine their SPF requirements into **one** SPF record rather than adding another `v=spf1` record. Review existing MX records before replacing them.

### Verification and troubleshooting

Check public DNS:

```sh
dig +short MX pushkarghanekar.com
dig +short TXT pushkarghanekar.com

# Query a public resolver if local DNS appears stale.
dig @1.1.1.1 +short MX pushkarghanekar.com
```

Then verify the domain and alias status in ImprovMX and send a test from a different email account to `hello@pushkarghanekar.com`. Confirm it arrives in Gmail; DNS verification alone does not prove delivery. If mail is missing, check DNS propagation, the forwarding destination, spam folders, and any delivery diagnostics available in ImprovMX.

To change the destination inbox, update the alias in ImprovMX. No website or DNS change is needed while using the same forwarding service.

### Website link

`_config.yml` holds the public address:

```yaml
email: hello@pushkarghanekar.com
```

`_includes/navigation.html` renders the `mailto:` link. Restart Jekyll after changing the config and deploy the site to publish website changes. No private destination is included in the generated pages.

### Replying without exposing Gmail

**This setup is inbound forwarding only.** A normal reply from Gmail can reveal the Gmail address. Sending as `hello@pushkarghanekar.com` requires an outbound email provider and authenticated SMTP configured in Gmail under **Settings → Accounts and Import → Send mail as**. Outbound SMTP was not configured as part of this setup.

Before using the alias for replies, follow the outbound provider's SPF/DKIM instructions, configure DMARC appropriately, and test the sender and reply-to addresses from another inbox. Keep SMTP credentials out of this repository.

## AI tag classification

`_posts/classify_tags.py` uses OpenRouter's Jev Decisions API to suggest tags from this set: `writing`, `ai`, `science`, `life`, `coding`, `agents`, `automation`, `travel`, and `papers`.

```sh
export OPENROUTER_API_KEY="..."
python _posts/classify_tags.py          # preview all suggestions
python _posts/classify_tags.py --write  # update front matter
```

Use `--file filename.md` to classify one post. The default confidence threshold is 75%; override it with `--threshold`. Preview first: `--write` replaces existing tags. Post text is sent to OpenRouter, so only use this on material you intend to share.
