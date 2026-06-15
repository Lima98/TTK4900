#!/usr/bin/env python3
"""Render compact appendix previews of the example archive webpage.

The full archive page is too tall to include comfortably in the thesis appendix.
This script extracts a few representative sections from ``webpage/index.html``,
rewrites local asset paths so they resolve inside the repository, swaps PDF
embeds for PNG previews, and renders three static HTML pages that can be
thumbnail-rendered with Quick Look.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "webpage" / "index.html"
PREVIEW_HTML_DIR = ROOT / "webpage" / "preview"
OUTPUT_DIR = ROOT / "thesis" / "latex" / "Figures" / "appendix"
TMP_RENDER_DIR = Path("/private/tmp")
RENDER_SIZE = "2200"


PREVIEWS = (
    {
        "name": "archive_preview_top",
        "include_hero": True,
        "chapter_ids": ("chapter-2-2",),
    },
    {
        "name": "archive_preview_first",
        "include_hero": False,
        "chapter_ids": ("chapter-3-3",),
    },
    {
        "name": "archive_preview_second",
        "include_hero": False,
        "chapter_ids": ("chapter-4-3",),
    },
    {
        "name": "archive_preview_iter3",
        "include_hero": False,
        "chapter_ids": ("chapter-5-4",),
    },
)


def main() -> None:
    html_only = "--html-only" in sys.argv
    html = INDEX.read_text(encoding="utf-8")
    style = extract(r"<style>(?P<body>.*?)</style>", html)
    hero = extract(r"(<header class=\"hero\">.*?</header>)", html)
    sidebar = extract(r"(<nav class=\"sidebar\".*?</nav>)", html)
    chapters = {
        match.group("id"): match.group(0)
        for match in re.finditer(
            r"<section class=\"chapter\" id=\"(?P<id>[^\"]+)\">.*?</section>",
            html,
            re.S,
        )
    }

    PREVIEW_HTML_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for preview in PREVIEWS:
        chapter_html = "\n".join(chapters[chapter_id] for chapter_id in preview["chapter_ids"])
        page = build_preview_page(
            style=style,
            hero=hero if preview["include_hero"] else "",
            sidebar=sidebar,
            chapter_html=chapter_html,
            include_hero=preview["include_hero"],
        )
        preview_path = PREVIEW_HTML_DIR / f"{preview['name']}.html"
        preview_path.write_text(page, encoding="utf-8")
        print(f"Wrote {preview_path.relative_to(ROOT)}")
        if not html_only:
            render_preview_png(preview_path, OUTPUT_DIR / f"{preview['name']}.png")
            print(f"Rendered {preview_path.relative_to(ROOT)}")


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.S)
    if not match:
        raise RuntimeError(f"Could not find pattern: {pattern}")
    return match.group("body") if "body" in match.groupdict() else match.group(1)


def build_preview_page(
    *,
    style: str,
    hero: str,
    sidebar: str,
    chapter_html: str,
    include_hero: bool,
) -> str:
    localized_sidebar = localize_fragment(sidebar)
    localized_chapters = localize_fragment(chapter_html)

    layout_style = "" if include_hero else ' style="margin-top: 2rem;"'

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Archive Preview</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{style}

      img.score-pdf {{
        object-fit: cover;
        object-position: top left;
      }}
    </style>
  </head>
  <body id="top">
    {localize_fragment(hero) if hero else ""}
    <div class="layout"{layout_style}>
      {localized_sidebar}
      <main class="content">
        {localized_chapters}
      </main>
    </div>
  </body>
</html>
"""


def localize_fragment(fragment: str) -> str:
    localized = replace_embeds_with_images(fragment)

    def replace_attr(match: re.Match[str]) -> str:
        attr = match.group("attr")
        value = match.group("value")
        if value.startswith("#") or value.startswith(("http://", "https://", "file://")):
            return match.group(0)
        if value.startswith("thesis-examples/"):
            resolved = local_example_path(value.removeprefix("thesis-examples/"))
            return f'{attr}="{resolved.as_uri()}"'
        if value == "thesis/main.pdf":
            return f'{attr}="{(ROOT / "thesis" / "latex" / "main.pdf").as_uri()}"'
        if value == "docs/index.html":
            candidate = ROOT / "docs" / "index.html"
            if not candidate.exists():
                candidate = ROOT / "docs" / "_build" / "html" / "index.html"
            return f'{attr}="{candidate.as_uri()}"'
        return match.group(0)

    return re.sub(r'(?P<attr>href|src)="(?P<value>[^"]+)"', replace_attr, localized)


def replace_embeds_with_images(fragment: str) -> str:
    def repl(match: re.Match[str]) -> str:
        relative = match.group("path").removeprefix("thesis-examples/")
        png_path = ensure_png_preview(local_example_path(relative))
        return f'<img class="score-pdf" src="{png_path.as_uri()}" alt="Score preview">'

    return re.sub(
        r'<embed class="score-pdf" src="(?P<path>thesis-examples/[^"#]+)\#[^"]*" type="application/pdf">',
        repl,
        fragment,
    )


def local_example_path(relative: str) -> Path:
    return ROOT / "thesis" / "latex" / "examples" / relative


def ensure_png_preview(pdf_path: Path) -> Path:
    if pdf_path.suffix != ".pdf":
        return pdf_path
    png_path = pdf_path.with_suffix(".png")
    if png_path.exists():
        return png_path
    subprocess.run(
        ["mutool", "draw", "-F", "png", "-o", str(png_path), str(pdf_path), "1"],
        check=True,
    )
    return png_path


def render_preview_png(preview_html: Path, output_png: Path) -> None:
    subprocess.run(
        ["qlmanage", "-t", "-s", RENDER_SIZE, "-o", str(TMP_RENDER_DIR), str(preview_html)],
        check=True,
    )
    tmp_png = TMP_RENDER_DIR / f"{preview_html.name}.png"
    if not tmp_png.exists():
        raise RuntimeError(f"Quick Look did not produce {tmp_png}")
    shutil.copy2(tmp_png, output_png)


if __name__ == "__main__":
    main()
