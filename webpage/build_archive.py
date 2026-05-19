#!/usr/bin/env python3
"""Build the thesis example archive from the LaTeX source.

The archive page should mirror the examples that are actually present in the
thesis. This script reads the ``example`` environments from the chapter files,
uses ``main.aux`` for the resolved example numbers and printed page numbers,
and writes ``webpage/index.html``.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from melody_engine.lilypond import render_sources

WEBPAGE_DIR = ROOT / "webpage"
THESIS_DIR = ROOT / "thesis" / "latex"
THESIS_SOURCE_EXAMPLES = ROOT / "thesis" / "examples"
CHAPTER_DIR = THESIS_DIR / "Chapters"
MAIN_AUX = THESIS_DIR / "main.aux"
OUTPUT = WEBPAGE_DIR / "index.html"
PDF_PAGE_OFFSET = 11


SECTION_TITLES = {
    "2.2": "Music Theory Examples",
    "6.1": "First Iteration Results",
    "6.2": "Second Iteration Results",
}


SECTION_DESCRIPTIONS = {
    "2.2": "Examples related to scales, harmony, and interval structure.",
    "6.1": "Examples from the first melody-generation iteration.",
    "6.2": "Examples from the second melody-generation iteration.",
}


@dataclass(frozen=True)
class AuxLabel:
    number: str
    printed_page: int
    caption: str


@dataclass(frozen=True)
class Example:
    number: str
    printed_page: int
    title: str
    label: str
    pdf: Path
    wav: Path | None
    ratio: float
    tags: tuple[str, ...]

    @property
    def section(self) -> str:
        return ".".join(self.number.split(".")[:2])

    @property
    def pdf_page(self) -> int:
        return self.printed_page + PDF_PAGE_OFFSET


def main() -> None:
    labels = read_aux_labels(MAIN_AUX)
    examples = collect_examples(labels)
    OUTPUT.write_text(render_page(examples), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(examples)} example(s).")
    missing_audio = [example.number for example in examples if example.wav is None]
    if missing_audio:
        print(f"Missing WAV audio for: {', '.join(missing_audio)}")


def read_aux_labels(path: Path) -> dict[str, AuxLabel]:
    labels: dict[str, AuxLabel] = {}
    pattern = re.compile(
        r"\\newlabel\{(?P<label>fig:[^}]+)\}\{\{(?P<number>[^}]+)\}"
        r"\{(?P<page>\d+)\}\{(?P<caption>.*?)\}\{example\.[^}]+\}\{\}\}"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if match:
            labels[match.group("label")] = AuxLabel(
                number=match.group("number"),
                printed_page=int(match.group("page")),
                caption=clean_latex(match.group("caption")),
            )
    return labels


def collect_examples(labels: dict[str, AuxLabel]) -> list[Example]:
    examples: list[Example] = []
    for chapter in sorted(CHAPTER_DIR.glob("*.tex")):
        text = chapter.read_text(encoding="utf-8")
        for body in re.findall(r"\\begin\{example\}(?:\[[^\]]+\])?(.*?)\\end\{example\}", text, re.S):
            label_match = re.search(r"\\label\{(?P<label>fig:[^}]+)\}", body)
            image_match = re.search(r"\\includegraphics(?:\[[^\]]+\])?\{(?P<path>[^}]+)\}", body)
            if not label_match or not image_match:
                continue
            label = label_match.group("label")
            if label not in labels:
                continue

            pdf = THESIS_DIR / image_match.group("path")
            if not pdf.exists():
                continue

            aux = labels[label]
            title = aux.caption or caption_from_body(body)
            wav = find_audio_for_score(pdf)
            examples.append(
                Example(
                    number=aux.number,
                    printed_page=aux.printed_page,
                    title=title.rstrip("."),
                    label=label,
                    pdf=pdf,
                    wav=wav,
                    ratio=pdf_aspect_ratio(pdf),
                    tags=tags_for(pdf, aux.number),
                )
            )
    return sorted(examples, key=lambda example: tuple(int(part) for part in example.number.split(".")))


def caption_from_body(body: str) -> str:
    match = re.search(r"\\caption\{(?P<caption>.*?)\}", body, re.S)
    return clean_latex(match.group("caption")) if match else "Thesis example"


def clean_latex(value: str) -> str:
    replacements = {
        r"\musPitch": "",
        r"\musFlat": "flat",
        r"\fl": "flat",
        r"\textit": "",
        r"\textbf": "",
    }
    cleaned = value
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = re.sub(r"\\[a-zA-Z]+\*?", "", cleaned)
    cleaned = cleaned.replace("{", "").replace("}", "")
    cleaned = cleaned.replace("~", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def pdf_aspect_ratio(path: Path) -> float:
    try:
        result = subprocess.run(
            ["mutool", "info", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return 3.0

    match = re.search(r"Mediaboxes.*?\[\s*0\s+0\s+(?P<width>[\d.]+)\s+(?P<height>[\d.]+)\s*\]", result.stdout, re.S)
    if not match:
        return 3.0
    width = float(match.group("width"))
    height = float(match.group("height"))
    if height <= 0:
        return 3.0
    return max(1.4, min(width / height, 6.5))


def find_audio_for_score(pdf: Path) -> Path | None:
    """Find the WAV file that belongs to a cropped score PDF.

    Thesis score PDFs are usually named ``name.cropped.pdf`` while their audio
    files are named ``name.wav``. Keep a fallback for direct ``name.pdf`` to
    ``name.wav`` matching so future examples can use either convention.
    """
    candidates: list[Path] = []
    if pdf.name.endswith(".cropped.pdf"):
        candidates.append(pdf.with_name(pdf.name.removesuffix(".cropped.pdf") + ".wav"))
    candidates.append(pdf.with_suffix(".wav"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    generated = render_missing_audio(pdf)
    if generated is not None:
        return generated
    return None


def render_missing_audio(pdf: Path) -> Path | None:
    """Render missing WAV audio from the matching thesis example source if it exists."""
    source = source_for_score(pdf)
    if source is None:
        return None

    try:
        render_sources([source], output_dir=pdf.parent, wav=True)
    except RuntimeError as error:
        print(f"Could not render audio for {pdf.relative_to(THESIS_DIR)}: {error}")
        return None
    return find_existing_audio(pdf)


def source_for_score(pdf: Path) -> Path | None:
    """Return the matching ``thesis/examples`` LilyPond source for a score PDF."""
    relative = pdf.relative_to(THESIS_DIR / "examples")
    stem = relative.name.removesuffix(".cropped.pdf").removesuffix(".pdf")
    source = THESIS_SOURCE_EXAMPLES / relative.parent / f"{stem}.ly"
    return source if source.exists() else None


def find_existing_audio(pdf: Path) -> Path | None:
    candidates: list[Path] = []
    if pdf.name.endswith(".cropped.pdf"):
        candidates.append(pdf.with_name(pdf.name.removesuffix(".cropped.pdf") + ".wav"))
    candidates.append(pdf.with_suffix(".wav"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def tags_for(pdf: Path, number: str) -> tuple[str, ...]:
    path_text = pdf.as_posix().lower()
    tags: list[str] = []
    if "04theory" in path_text:
        tags.append("Theory")
    if "iter1" in path_text:
        tags.append("Iteration 1")
    if "iter2" in path_text:
        tags.append("Iteration 2")
    if "scale" in path_text:
        tags.append("Scale")
    if "interval" in path_text:
        tags.append("Intervals")
    if "register" in path_text:
        tags.append("Range")
    if "voices" in path_text:
        tags.append("Multi-Voice")
    if "melody" in path_text:
        tags.append("Melody")
    if not tags:
        tags.append(f"Section {'.'.join(number.split('.')[:2])}")
    return tuple(tags)


def rel(path: Path) -> str:
    return path.relative_to(THESIS_DIR / "examples").as_posix()


def render_page(examples: list[Example]) -> str:
    sections = group_by_section(examples)
    nav = "\n".join(
        f'        <a href="#chapter-{section.replace(".", "-")}">Section {section} - {html.escape(section_title(section))}</a>'
        for section in sections
    )
    section_html = "\n\n".join(render_section(section, items) for section, items in sections.items())
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Procedural Generation: Music - Thesis Example Archive</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{STYLE}
    </style>
  </head>
  <body>
    <header class="hero">
      <div class="hero-inner">
        <div class="hero-copy">
          <h1>Procedural Generation:<br>Music Thesis Archive</h1>
          <p>A browsable collection of the numbered musical examples referenced throughout the thesis.</p>
          <div class="hero-actions">
            <a class="primary" href="thesis/main.pdf" target="_blank" rel="noopener noreferrer">Open Thesis PDF</a>
            <a href="docs/index.html">Open Technical Documentation</a>
          </div>
        </div>
        <aside class="hero-note">
          <h2>Archive Overview</h2>
          <ul>
            <li>Example numbers match the numbering used in the thesis.</li>
            <li>Each card contains a score preview, a short description, and audio playback when available.</li>
            <li>Examples are grouped by the same sections used in the written thesis.</li>
          </ul>
        </aside>
      </div>
    </header>

    <div class="layout">
      <nav class="sidebar" aria-label="Page sections">
        <h2>Navigate</h2>
{nav}
      </nav>

      <main class="content">
{section_html}
      </main>
    </div>

    <footer>© 2026 - Jan-Øivind Lima</footer>
  </body>
</html>
"""


def group_by_section(examples: list[Example]) -> dict[str, list[Example]]:
    grouped: dict[str, list[Example]] = {}
    for example in examples:
        grouped.setdefault(example.section, []).append(example)
    return grouped


def section_title(section: str) -> str:
    return SECTION_TITLES.get(section, f"Section {section} Examples")


def section_description(section: str) -> str:
    return SECTION_DESCRIPTIONS.get(section, "Examples referenced in this thesis section.")


def render_section(section: str, examples: list[Example]) -> str:
    cards = "\n\n".join(render_card(example) for example in examples)
    section_id = section.replace(".", "-")
    return f"""        <section class="chapter" id="chapter-{section_id}">
          <div class="chapter-header">
            <span>Section {html.escape(section)}</span>
            <h2>{html.escape(section_title(section))}</h2>
            <p>{html.escape(section_description(section))}</p>
          </div>

          <div class="example-grid">
{cards}
          </div>
        </section>"""


def render_card(example: Example) -> str:
    tags = "\n".join(f"                    <span>{html.escape(tag)}</span>" for tag in example.tags)
    audio = (
        f"""                <audio controls>
                  <source src="thesis-examples/{html.escape(rel(example.wav))}" type="audio/wav">
                </audio>"""
        if example.wav
        else '                <p class="audio-missing">No WAV file is currently available for this example.</p>'
    )
    return f"""            <article class="example-card" id="example-{example.number.replace(".", "-")}">
              <div class="example-top">
                <div class="example-heading">
                  <p class="example-number">{html.escape(example.number)}</p>
                  <h3>{html.escape(example.title)}</h3>
                  <div class="meta">
{tags}
                  </div>
                </div>
                <div class="example-links">
                  <a href="thesis/main.pdf#page={example.pdf_page}" target="_blank" rel="noopener noreferrer">Find In Thesis</a>
                </div>
              </div>
              <div class="example-media" style="--score-ratio: {example.ratio:.4f};">
                <div class="score-frame">
                  <a class="score-link" href="thesis-examples/{html.escape(rel(example.pdf))}" target="_blank" rel="noopener noreferrer" aria-label="Open Example {html.escape(example.number)} score PDF">
                    <embed class="score-pdf" src="thesis-examples/{html.escape(rel(example.pdf))}#toolbar=0&navpanes=0&scrollbar=0&view=FitH&zoom=page-width" type="application/pdf">
                  </a>
                </div>
              </div>
              <div class="example-body">
                <p>{html.escape(example.title)}.</p>
{audio}
              </div>
            </article>"""


STYLE = """      :root {
        --bg: #f3efe7;
        --paper: #fffdf8;
        --ink: #1f1a17;
        --muted: #6d625a;
        --line: #d7c8b8;
        --accent: #8a4b2a;
        --accent-soft: #ead6c6;
        --shadow: 0 18px 40px rgba(64, 42, 27, 0.09);
      }

      * { box-sizing: border-box; }

      html { scroll-behavior: smooth; }

      body {
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        color: var(--ink);
        background:
          radial-gradient(circle at top left, rgba(138, 75, 42, 0.08), transparent 30%),
          linear-gradient(180deg, #f7f2ea 0%, var(--bg) 40%, #efe7da 100%);
        line-height: 1.6;
      }

      a { color: inherit; }

      .hero { padding: 4rem 1.5rem 2.5rem; }

      .hero-inner {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        gap: 1.5rem;
        grid-template-columns: 1.4fr 0.9fr;
        align-items: start;
      }

      .hero-copy h1 {
        margin: 0;
        font-size: clamp(2.2rem, 5vw, 4.6rem);
        line-height: 0.95;
        letter-spacing: -0.04em;
      }

      .hero-copy p {
        max-width: 60ch;
        margin: 1.2rem 0 0;
        font-size: 1.05rem;
        color: var(--muted);
      }

      .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-top: 1.5rem;
      }

      .hero-actions a {
        text-decoration: none;
        padding: 0.8rem 1.1rem;
        border-radius: 999px;
        font-size: 0.95rem;
        border: 1px solid var(--line);
        background: rgba(255, 253, 248, 0.85);
      }

      .hero-actions a.primary {
        background: var(--accent);
        color: white;
        border-color: var(--accent);
      }

      .hero-note {
        background: rgba(255, 253, 248, 0.78);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.4rem;
        box-shadow: var(--shadow);
      }

      .hero-note h2 {
        margin-top: 0;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .hero-note ul {
        margin: 0.8rem 0 0;
        padding-left: 1.2rem;
        color: var(--muted);
      }

      .layout {
        max-width: 1200px;
        margin: 0 auto 4rem;
        padding: 0 1.5rem;
        display: grid;
        grid-template-columns: 260px minmax(0, 1fr);
        gap: 2rem;
      }

      .sidebar {
        position: sticky;
        top: 1rem;
        align-self: start;
        background: rgba(255, 253, 248, 0.8);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1rem;
        box-shadow: var(--shadow);
      }

      .sidebar h2 {
        margin: 0 0 0.8rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .sidebar a {
        display: block;
        text-decoration: none;
        padding: 0.7rem 0.8rem;
        border-radius: 14px;
        color: var(--muted);
      }

      .sidebar a:hover,
      .sidebar a:focus {
        background: var(--accent-soft);
        color: var(--ink);
      }

      .content { min-width: 0; }

      .chapter { margin-bottom: 3rem; }

      .chapter-header { margin-bottom: 1rem; }

      .chapter-header span {
        display: inline-block;
        margin-bottom: 0.5rem;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .chapter-header h2 {
        margin: 0;
        font-size: clamp(1.6rem, 2vw, 2.3rem);
      }

      .chapter-header p {
        margin: 0.7rem 0 0;
        color: var(--muted);
        max-width: 72ch;
      }

      .example-grid {
        display: grid;
        gap: 1.2rem;
      }

      .example-card {
        display: grid;
        gap: 1rem;
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.2rem;
        box-shadow: var(--shadow);
      }

      .example-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
      }

      .example-heading {
        min-width: 0;
        display: grid;
        gap: 0.55rem;
      }

      .example-heading h3 {
        margin: 0;
        font-size: 1rem;
        color: var(--muted);
        font-weight: normal;
      }

      .example-number {
        margin: 0;
        font-size: clamp(1.8rem, 2.8vw, 2.6rem);
        line-height: 0.95;
        letter-spacing: -0.04em;
      }

      .meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
      }

      .meta span {
        font-size: 0.85rem;
        padding: 0.35rem 0.65rem;
        border-radius: 999px;
        background: #f5ece2;
        color: #5c4335;
      }

      .example-links {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
      }

      .example-links a {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        min-width: 148px;
        padding: 0.65rem 1rem;
        border-radius: 999px;
        border: 1px solid var(--line);
        background: white;
        font-size: 0.92rem;
        white-space: nowrap;
      }

      .example-media {
        width: 100%;
        aspect-ratio: var(--score-ratio);
        min-height: 140px;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: #fbf8f2;
        overflow: hidden;
      }

      .score-frame {
        width: 100%;
        height: 100%;
        overflow: hidden;
      }

      .score-link {
        display: block;
        width: 100%;
        height: 100%;
      }

      .score-pdf {
        display: block;
        width: 112%;
        height: 112%;
        margin-left: -6%;
        margin-top: -3%;
        border: 0;
        background: white;
      }

      .example-body {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 320px;
        gap: 1rem;
        align-items: start;
      }

      .example-body p {
        margin: 0;
        color: var(--muted);
      }

      audio { width: 100%; }

      .audio-missing {
        padding: 0.75rem 0.9rem;
        border: 1px dashed var(--line);
        border-radius: 14px;
        background: #fbf8f2;
      }

      footer {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1.5rem 3rem;
        color: var(--muted);
      }

      @media (max-width: 980px) {
        .hero-inner,
        .layout,
        .example-body {
          grid-template-columns: 1fr;
        }

        .sidebar { position: static; }

        .example-top { flex-direction: column; }
      }"""


if __name__ == "__main__":
    main()
