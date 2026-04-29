# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Jekyll blog deployed via GitHub Pages for **hmpgr**, a B2B website audit tool. Posts target B2B SaaS founders and marketing managers, focused on homepage conversion optimization. Most content is generated automatically; humans review and merge.

## Architecture

Two pieces only:

1. **`scripts/generate_post.py`** — Python script that calls the Gemini API (`gemini-2.0-flash-lite`) to draft one Jekyll-formatted Markdown post into `_posts/YYYY-MM-DD-<slug>.md`. The brand voice, target audience, and post structure (Jekyll front matter, H2/H3 sections, "Pro Tip" block, hmpgr.com CTA) are all baked into the prompt inside this script — edit the prompt here to change tone or required sections. It also reads the last 5 filenames from `_posts/` and passes them to the model so it avoids repeating recent topics.

2. **`.github/workflows/blank.yml`** — GitHub Action that runs the script every Monday at 09:00 UTC (also `workflow_dispatch` for manual runs), then uses `peter-evans/create-pull-request@v6` to open a PR on a `draft/weekly-post-<run_id>` branch labeled `automated-content` with @aonghusflynn as reviewer. Merging the PR publishes the post via GitHub Pages.

The Jekyll site itself isn't checked in here yet — there's no `_config.yml`, `Gemfile`, layouts, or existing `_posts/` directory in the repo. GitHub Pages builds with default settings until those land.

## Running the generator locally

```bash
pip install google-generativeai
GEMINI_API_KEY=<key> python scripts/generate_post.py
```

The script writes to `_posts/` relative to the working directory and will fail if that directory doesn't exist (the workflow runs from repo root where `_posts/` is expected to exist after first publish).

Required secret in GitHub Actions: `GEMINI_API_KEY`.
