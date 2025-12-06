---
layout: page
title: Archive
permalink: /archive/
---

## Posts by Year

{% for year in site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
  <h3>{{ year.name }}</h3>
  <ul>
    {% for post in year.items %}
      <li>
        <span class="post-meta">{{ post.date | date: "%b %-d" }}</span>
        <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      </li>
    {% endfor %}
  </ul>
{% endfor %}
