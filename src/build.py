"""Build the Fors-Automation hub site.

Reads project metadata from ``src/data/projects.yaml``, renders the Jinja2
templates in ``src/templates/``, copies ``static/`` into ``dist/``, and writes
the resulting static site to ``dist/``.

Run from the repo root:

    python src/build.py
"""

from __future__ import annotations

import datetime
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Paths are resolved relative to the repo root (this file's parent's parent),
# so the build works regardless of the current working directory.
ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "src" / "templates"
DATA_FILE = ROOT / "src" / "data" / "projects.yaml"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"


def load_data() -> dict:
    """Load site metadata and the project list from YAML."""
    with DATA_FILE.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def clean_dist() -> None:
    """Remove any previous build so dist/ only contains fresh output."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)


def copy_static() -> None:
    """Copy static assets (CSS, JS, images) into dist/."""
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, DIST_DIR, dirs_exist_ok=True)


def render_site(data: dict) -> None:
    """Render templates and write the generated HTML into dist/."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    context = {
        "site": data.get("site", {}),
        "projects": data.get("projects", []),
        "year": datetime.date.today().year,
    }

    template = env.get_template("index.html")
    (DIST_DIR / "index.html").write_text(template.render(context), encoding="utf-8")

    # Stop GitHub Pages from running Jekyll over the output (which would ignore
    # files/folders beginning with an underscore).
    (DIST_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    data = load_data()
    clean_dist()
    copy_static()
    render_site(data)
    project_count = len(data.get("projects", []))
    print(f"Built {project_count} project(s) into {DIST_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
