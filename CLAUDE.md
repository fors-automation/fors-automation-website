# Project: Fors-Automation Hub Site

A static website listing all projects under Fors-Automation with links to external
sites and app downloads.

## Status
Greenfield — not yet scaffolded. The structure below is the **target** design.
First task is to create `src/build.py`, `src/templates/`, `src/data/projects.yaml`,
and `static/`. Until those exist, treat paths below as where things should go.

## Stack
- Python 3.11+ with a virtualenv
- Jinja2 (templating) + PyYAML (data) — keep dependencies to these two where possible
- Output: static HTML/CSS/JS in `/dist` (gitignored; never edit by hand)
- Deployed via GitHub Pages using a GitHub Actions workflow

## Structure
- `src/build.py` — main build script (reads YAML, renders templates, writes `dist/`)
- `src/templates/` — Jinja2 templates
- `src/data/projects.yaml` — project metadata (name, description, links, icons)
- `static/` — CSS, JS, images (copied into `dist/` by the build)
- `dist/` — build output; gitignored, produced by `build.py`, published by CI

## Commands
```bash
# one-time setup
python -m venv .venv
source .venv/Scripts/activate   # Git Bash on Windows
# .venv\Scripts\Activate.ps1    # PowerShell alternative
pip install -r requirements.txt

# build the site into dist/
python src/build.py

# preview locally
python -m http.server -d dist 8000   # then open http://localhost:8000
```

## Conventions
- Add or change projects by editing `src/data/projects.yaml` — never hand-write
  per-project HTML.
- `dist/` is generated output: don't edit it directly and don't commit it.
- Keep the build dependency-light (Jinja2 + PyYAML only) unless there's a strong reason.

## projects.yaml schema
Each entry under `projects:` (illustrative — adjust as the real schema settles):
```yaml
projects:
  - name: "Example App"
    category: "Tools"                    # Games | Tools | Resources
    description: "One-line summary of what it does."
    url: "https://example.com"          # external site (optional)
    download: "https://.../app.zip"      # app download (optional)
    icon: "static/img/example.png"       # optional
```

## Deployment
GitHub Actions installs deps, runs `python src/build.py`, and publishes `dist/` to
GitHub Pages. `dist/` is intentionally gitignored — it is built in CI, not committed.
Hosting may move later; keep `build.py` host-agnostic (relative asset paths).
