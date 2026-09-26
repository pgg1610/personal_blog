---
layout: default
title: Blog
description: Notes on science, technology, and the work of making medicines.
permalink: /blog/
---
<header class="page-header">
  <h1>Blog</h1>
  <p class="lede">Notes on science, technology, and making medicines.</p>
</header>

<section aria-labelledby="writing-heading">
  <div class="section-heading">
    <h2 id="writing-heading">All writing</h2>
    <a href="{{ '/feed.xml' | relative_url }}">Subscribe via RSS</a>
  </div>
  <ul class="post-list">
    {% for post in site.posts %}
      <li>
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: '%b %Y' }}</time>
        <div>
          <h3><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
        </div>
      </li>
    {% endfor %}
  </ul>
</section>
