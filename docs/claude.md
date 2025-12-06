# HMPGR Blog - Claude Context

## Project Overview
This is a Jekyll-based blog for HMPGR (blog.hmpgr.com), providing advice on running websites for small businesses, with a focus on B2B SaaS homepage optimization and conversion strategies.

## Project Structure

### Core Configuration
- **Jekyll Version**: Using `github-pages` gem for compatibility
- **Site URL**: https://blog.hmpgr.com
- **Permalink Structure**: `/:year/:month/:title/`
- **Markdown Engine**: kramdown

### Key Directories
- `_posts/`: Blog posts (17+ posts, all dated 2025-12-03)
- `_layouts/`: Layout templates
  - `default.html`: Main site template with header/footer
  - `home.html`: Homepage layout
  - `post.html`: Individual post layout
  - `page.html`: Static page layout
  - `archive-*.html`: Archive layouts (year, month, category, tag)
- `_includes/`: Reusable components
  - `header.html`: Navigation (Home, About, Archive)
  - `head.html`: HTML head section
  - `google-analytics.html`: Analytics tracking
- `assets/`: CSS and static assets

### Active Plugins
1. `jekyll-feed` - RSS feed generation
2. `jekyll-sitemap` - Sitemap generation
3. `jekyll-archives` - Archive page generation
   - Enabled: year, month, categories, tags
   - Permalinks:
     - Year: `/archive/:year/`
     - Month: `/archive/:year/:month/`
     - Category: `/category/:name/`
     - Tag: `/tag/:name/`

### Navigation Structure
- Home (/)
- About (/about)
- Archive (/archive) - Lists all posts grouped by year

### Content Categories
Posts focus on B2B SaaS homepage optimization:
- Homepage conversion strategies
- Above-the-fold content
- SEO and schema markup
- Call-to-action hierarchy
- Value proposition messaging

## Development Workflow

### Running the Site Locally
```bash
cd docs
bundle exec jekyll serve
```

### Important Notes
- **Jekyll Config**: Changes to `_config.yml` require server restart
- **Git Worktree**: This is a worktree at `/Users/aonghusflynn/.claude-worktrees/docs/vibrant-gagarin`
- **Main Repo**: `/Users/aonghusflynn/Projects/blog-hmpgr/docs`
- **Current Branch**: `vibrant-gagarin`
- **Main Branch**: `main`

### Post Front Matter Structure
```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
categories: category1 category2
---
```

## Common Tasks

### Creating a New Post
1. Create file in `_posts/` with format: `YYYY-MM-DD-post-slug.markdown`
2. Add front matter with layout, title, date, categories
3. Write content in Markdown

### Modifying Navigation
Edit `_layouts/default.html` lines 22-26 for navigation links

### Archive Configuration
Archive settings are in `_config.yml` lines 37-53. To modify archive types or permalinks, edit the `jekyll-archives` section.

## Design & Styling
- Custom fonts: Crimson Pro, Work Sans, JetBrains Mono (via Google Fonts)
- Styles: `/assets/css/style.css`
- Responsive design with container-based layout

## Contact & Social
- Email: admin@hmpgr.com
- Twitter: @aonghusflynn
- GitHub: aonghusflynn

## Recent Changes
- Fixed archive functionality by correcting plugin name from `jekyll-archive` to `jekyll-archives`
- Added complete jekyll-archives configuration
- Created archive page and all necessary archive layout templates
- Archive page now properly displays posts grouped by year
