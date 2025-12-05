# Refined Brutalist Jekyll Theme

A modern Jekyll theme with strong typography, clean layouts, and a distinctive aesthetic.

## Features

- **Bold Typography**: Crimson Pro for headings, Work Sans for body text
- **High Contrast**: Clean black/white with warm amber accents
- **Smooth Animations**: Subtle fade-ins and micro-interactions
- **Responsive Design**: Mobile-optimized layouts
- **Code-Friendly**: Syntax highlighting with JetBrains Mono
- **HMPGR CTA**: Integrated call-to-action on homepage and post pages

## Quick Start

1. Update `_config.yml` with your site information
2. Add posts to `_posts/` directory (format: `YYYY-MM-DD-title.md`)
3. Run locally: `bundle exec jekyll serve`
4. Push to GitHub - your site will build automatically

## Structure

```
├── _config.yml           # Site configuration
├── _layouts/
│   ├── default.html      # Base layout
│   ├── home.html         # Homepage layout
│   └── post.html         # Blog post layout
├── _posts/               # Your blog posts go here
├── assets/
│   └── css/
│       └── style.css     # Main stylesheet
├── about.md              # About page
└── index.html            # Homepage
```

## Customization

### Colors

Edit CSS variables in `assets/css/style.css`:

```css
:root {
  --color-accent: #FF6B35;  /* Change accent color */
  --color-text: #1A1A1A;    /* Main text color */
  --color-bg: #FAFAFA;      /* Background color */
}
```

### Fonts

Replace Google Fonts URLs in `_layouts/default.html` to use different typefaces.

### Navigation

Update navigation links in `_layouts/default.html`:

```html
<nav class="site-nav">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <!-- Add more links here -->
</nav>
```

### CTA

Edit the CTA text in `_layouts/home.html` and `_layouts/post.html` to customize the HMPGR call-to-action.

## Writing Posts

Create a new file in `_posts/` with format `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Your Post Title"
date: 2024-12-05 10:00:00 -0000
---

Your content here...
```

## Local Development

```bash
# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# View at http://localhost:4000
```

## License

Free to use and modify for your personal or commercial projects.
