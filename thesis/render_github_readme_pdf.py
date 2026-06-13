from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


RE_LINK_OR_CODE = re.compile(r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)")
RE_TABLE_DIVIDER = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+\s*$")
SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}


def escape_tex(text: str) -> str:
    text = text.replace("\u2013", "--")
    return "".join(SPECIALS.get(ch, ch) for ch in text)


def convert_inline(text: str) -> str:
    pieces: list[str] = []
    last = 0
    for match in RE_LINK_OR_CODE.finditer(text):
        pieces.append(escape_tex(text[last:match.start()]))
        code, label, url = match.groups()
        if code is not None:
            pieces.append(rf"\texttt{{{escape_tex(code)}}}")
        else:
            escaped_label = escape_tex(label)
            if url.startswith(("http://", "https://")):
                pieces.append(rf"\href{{{url}}}{{{escaped_label}}}")
            else:
                pieces.append(rf"\texttt{{{escaped_label}}}")
        last = match.end()
    pieces.append(escape_tex(text[last:]))
    return "".join(pieces)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(rows: list[list[str]]) -> str:
    columns = len(rows[0])
    if columns == 2:
        colspec = r"p{0.28\linewidth} p{0.62\linewidth}"
    else:
        width = 0.9 / max(columns, 1)
        colspec = " ".join(f"p{{{width:.2f}\\linewidth}}" for _ in range(columns))

    out = [r"\begin{center}", r"\small", rf"\begin{{tabular}}{{{colspec}}}", r"\toprule"]
    header = " & ".join(convert_inline(cell) for cell in rows[0]) + r" \\"
    out.append(header)
    out.append(r"\midrule")
    for row in rows[1:]:
        out.append(" & ".join(convert_inline(cell) for cell in row) + r" \\")
    out.extend([r"\bottomrule", r"\end{tabular}", r"\normalsize", r"\end{center}"])
    return "\n".join(out)


def render_markdown(markdown_path: Path, tex_dir: Path) -> str:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    i = 0
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(r"\end{itemize}")
            in_list = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped.startswith("```"):
            close_list()
            language = stripped.strip("`").strip()
            listing_opts = ["breaklines=true", "breakatwhitespace=true"]
            if language:
                listing_opts.append(f"language={language}")
            out.append(rf"\begin{{lstlisting}}[{','.join(listing_opts)}]")
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                out.append(lines[i])
                i += 1
            out.append(r"\end{lstlisting}")
            i += 1
            continue

        image_match = re.match(r"!\[[^\]]*\]\(([^)]+)\)", stripped)
        if image_match:
            close_list()
            image_path = (markdown_path.parent / image_match.group(1)).resolve()
            relative_image = os.path.relpath(image_path, tex_dir).replace(os.sep, "/")
            out.extend(
                [
                    r"\begin{center}",
                    rf"  \includegraphics[width=0.95\linewidth]{{{relative_image}}}",
                    r"\end{center}",
                ]
            )
            i += 1
            continue

        if stripped.startswith("# "):
            close_list()
            out.append(rf"\section*{{{convert_inline(stripped[2:].strip())}}}")
            i += 1
            continue

        if stripped.startswith("## "):
            close_list()
            out.append(rf"\subsection*{{{convert_inline(stripped[3:].strip())}}}")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and RE_TABLE_DIVIDER.match(lines[i + 1].strip()):
            close_list()
            rows = [split_table_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_table_row(lines[i].strip()))
                i += 1
            out.append(render_table(rows))
            continue

        if stripped.startswith("- "):
            if not in_list:
                out.append(r"\begin{itemize}")
                in_list = True
            out.append(rf"  \item {convert_inline(stripped[2:].strip())}")
            i += 1
            continue

        close_list()
        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            lookahead = lines[i].strip()
            if (
                not lookahead
                or lookahead.startswith(("```", "# ", "## ", "- ", "|"))
                or re.match(r"!\[[^\]]*\]\(([^)]+)\)", lookahead)
            ):
                break
            paragraph_lines.append(lookahead)
            i += 1
        out.append(convert_inline(" ".join(paragraph_lines)))

    close_list()
    return "\n\n".join(out)


def build_tex_body(markdown_path: Path, tex_dir: Path) -> str:
    content = render_markdown(markdown_path, tex_dir)
    return (
        r"\documentclass[a4paper,11pt]{article}" "\n"
        r"\usepackage[utf8]{inputenc}" "\n"
        r"\usepackage[T1]{fontenc}" "\n"
        r"\usepackage[margin=1in]{geometry}" "\n"
        r"\usepackage{graphicx}" "\n"
        r"\usepackage{booktabs}" "\n"
        r"\usepackage{array}" "\n"
        r"\usepackage{xcolor}" "\n"
        r"\usepackage{hyperref}" "\n"
        r"\usepackage{listings}" "\n"
        r"\setlength{\parindent}{0pt}" "\n"
        r"\setlength{\parskip}{0.6em}" "\n"
        r"\pagestyle{empty}" "\n"
        r"\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,breakatwhitespace=true,columns=fullflexible}" "\n"
        r"\begin{document}" "\n\n"
        + content
        + "\n\n"
        + r"\end{document}"
        + "\n"
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    markdown_path = repo_root / "README.md"
    output_dir = repo_root / "thesis" / "latex" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)

    tex_path = output_dir / "github_readme.generated.tex"
    tex_path.write_text(build_tex_body(markdown_path, output_dir), encoding="utf-8")

    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=output_dir,
        check=True,
    )

    for suffix in (".aux", ".log", ".out"):
        artifact = output_dir / f"github_readme.generated{suffix}"
        if artifact.exists():
            artifact.unlink()


if __name__ == "__main__":
    main()
