---
layout: default
title: Blog
description: Notes on science, technology, and the work of making medicines.
permalink: /blog/
search: true
animate: true
---
<header class="page-header">
  <h1>Blog</h1>
  <p class="lede">Notes on science, technology, and making medicines.</p>
  <p class="page-note">On writing and transparency: <a href="{{ '/llm-policy/' | relative_url }}">my LLM policy</a>. Browse writing by topic in the <a href="{{ '/tags/' | relative_url }}">tag index</a>, or subscribe via <a href="{{ '/feed.xml' | relative_url }}">RSS</a>.</p>
</header>

<section aria-labelledby="writing-heading">
  <h2 class="visually-hidden" id="writing-heading">All writing</h2>
  <form class="search-form" id="search-form" role="search" data-index="{{ '/search.json' | relative_url }}">
    <label class="visually-hidden" for="search-input">Search posts</label>
    <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
    <input class="search-input" id="search-input" type="search" name="q" placeholder="Search posts" autocomplete="off">
  </form>
  <p class="search-status" id="search-status" role="status" aria-live="polite"></p>
  <ul class="post-list post-list--intro" id="post-list">
    {% for post in site.posts %}
      <li style="--i: {{ forloop.index0 }}">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: '%B %-d, %Y' }}</time>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
      </li>
    {% endfor %}
  </ul>
</section>
