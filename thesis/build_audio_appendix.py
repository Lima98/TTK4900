#!/usr/bin/env python3
"""Build a standalone zip archive of thesis example audio."""

from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THESIS_DIR = ROOT / "thesis" / "latex"
CHAPTER_DIR = THESIS_DIR / "Chapters"
MAIN_AUX = THESIS_DIR / "main.aux"
OUTPUT_DIR = ROOT / "output"
OUTPUT_ZIP = OUTPUT_DIR / "example_audio_appendix.zip"


FILE_SECTION_PREFIX = {
    "04Music-theory.tex": "2.2",
    "05-First-iteration.tex": "3.3",
    "05-Second-iteration.tex": "4.3",
    "05-Third-iteration.tex": "5.4",
    "08Appendix.tex": "C",
}


SECTION_METADATA = {
    "2.2": "Section 2.2 - Music Theory",
    "3.3": "Section 3.3 - First Iteration Results",
    "4.3": "Section 4.3 - Second Iteration Results",
    "5.4": "Section 5.4 - Third Iteration Results",
    "C": "Appendix C - Additional Final Iteration Examples",
}


@dataclass(frozen=True)
class AuxLabel:
    number: str
    caption: str


@dataclass(frozen=True)
class ExampleAudio:
    number: str
    caption: str
    section: str
    wav: Path


def main() -> None:
    labels = read_aux_labels(MAIN_AUX)
    examples = collect_example_audio(labels)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        index_lines = ["Thesis Example Audio Appendix", "", "Files are grouped by thesis section and named by example number.", ""]
        for example in examples:
            folder = SECTION_METADATA.get(example.section, f"Section {example.section}")
            archive_path = Path("example_audio_appendix") / folder / f"{example.number}.wav"
            archive.write(example.wav, archive_path.as_posix())
            index_lines.append(f"{folder}/{example.number}.wav - {example.caption}")

        archive.writestr(
            "example_audio_appendix/README.txt",
            "\n".join(index_lines) + "\n",
        )

    print(f"Wrote {OUTPUT_ZIP.relative_to(ROOT)} with {len(examples)} audio file(s).")


def read_aux_labels(path: Path) -> dict[str, AuxLabel]:
    labels: dict[str, AuxLabel] = {}
    if not path.exists():
        return labels
    pattern = re.compile(
        r"\\newlabel\{(?P<label>fig:[^}]+)\}\{\{(?P<number>[^}]+)\}"
        r"\{[^}]+\}\{(?P<caption>.*?)\}\{example\.[^}]+\}\{\}\}"
    )
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if match:
            labels[match.group("label")] = AuxLabel(
                number=match.group("number"),
                caption=clean_latex(match.group("caption")),
            )
    return labels


def collect_example_audio(labels: dict[str, AuxLabel]) -> list[ExampleAudio]:
    examples: list[ExampleAudio] = []
    for chapter in sorted(CHAPTER_DIR.glob("*.tex")):
        section_prefix = FILE_SECTION_PREFIX.get(chapter.name)
        if section_prefix is None:
            continue

        text = chapter.read_text(encoding="utf-8")
        for index, body in enumerate(
            re.findall(r"\\begin\{example\}(?:\[[^\]]+\])?(.*?)\\end\{example\}", text, re.S),
            start=1,
        ):
            label_match = re.search(r"\\label\{(?P<label>fig:[^}]+)\}", body)
            image_match = re.search(r"\\includegraphics(?:\[[^\]]+\])?\{(?P<path>[^}]+)\}", body)
            if not label_match or not image_match:
                continue

            label = label_match.group("label")
            aux = labels.get(label)
            number = aux.number if aux is not None else inferred_number(section_prefix, index)
            caption = aux.caption if aux is not None and aux.caption else caption_from_body(body)

            pdf = THESIS_DIR / image_match.group("path")
            wav = wav_for_pdf(pdf)
            if wav is None or not wav.exists():
                continue

            examples.append(
                ExampleAudio(
                    number=number,
                    caption=caption,
                    section=section_from_number(number),
                    wav=wav,
                )
            )

    return sorted(examples, key=example_sort_key)


def inferred_number(section_prefix: str, index: int) -> str:
    return f"{section_prefix}.{index}"


def wav_for_pdf(pdf: Path) -> Path | None:
    candidates: list[Path] = []
    if pdf.name.endswith(".cropped.pdf"):
        candidates.append(pdf.with_name(pdf.name.removesuffix(".cropped.pdf") + ".wav"))
    candidates.append(pdf.with_suffix(".wav"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def section_from_number(number: str) -> str:
    parts = number.split(".")
    if parts and not parts[0].isdigit():
        return parts[0]
    return ".".join(parts[:2])


def example_sort_key(example: ExampleAudio) -> tuple[tuple[int, int | str], ...]:
    key: list[tuple[int, int | str]] = []
    for part in example.number.split("."):
        if part.isdigit():
            key.append((0, int(part)))
        else:
            key.append((1, part))
    return tuple(key)


def caption_from_body(body: str) -> str:
    match = re.search(r"\\caption(?:\[[^\]]*\])?\{(?P<caption>.*?)\}", body, re.S)
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
    cleaned = re.sub(r"\\cite[a-zA-Z]*\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\ref\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\examplelink(?:\[[^\]]*\])?", "", cleaned)
    cleaned = re.sub(r"\\[a-zA-Z]+\*?", "", cleaned)
    cleaned = cleaned.replace("{", "").replace("}", "")
    cleaned = cleaned.replace("~", " ")
    cleaned = re.sub(r"\s+\.", ".", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip().rstrip(".")


if __name__ == "__main__":
    main()
