from __future__ import annotations

"""Create a compact showcase figure for the procedural-generation intro section."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "thesis" / "latex" / "Figures" / "04theory" / "00_pcg_showcase.png"

PANELS = [
    (
        "organic growth",
        REPO_ROOT / "code" / ".proc-gen-examples" / "L_system" / "plant5.png",
    ),
    (
        "texture synthesis",
        REPO_ROOT / "thesis" / "latex" / "Figures" / "04theory" / "ex_sand.png",
    ),
    (
        "dungeon layout",
        REPO_ROOT / "code" / ".proc-gen-examples" / "binary-space-partitioning" / "figures" / "03_final_bsp_dungeon.png",
    ),
    (
        "terrain map",
        REPO_ROOT / "thesis" / "latex" / "Figures" / "04theory" / "ex_map.png",
    ),
]


def fit_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    source_w, source_h = image.size
    target_ratio = target_w / target_h
    source_ratio = source_w / source_h

    if source_ratio > target_ratio:
        new_h = target_h
        new_w = round(new_h * source_ratio)
    else:
        new_w = target_w
        new_h = round(new_w / source_ratio)

    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def build_showcase() -> None:
    card_w = 760
    card_h = 470
    title_h = 54
    gap = 36
    outer = 36

    canvas_w = outer * 2 + card_w * 2 + gap
    canvas_h = outer * 2 + card_h * 2 + gap
    canvas = Image.new("RGB", (canvas_w, canvas_h), "#ffffff")
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(34)

    for index, (title, path) in enumerate(PANELS):
        row = index // 2
        col = index % 2
        x = outer + col * (card_w + gap)
        y = outer + row * (card_h + gap)

        draw.rectangle((x, y, x + card_w, y + card_h), fill="#ffffff", outline="#222222", width=3)
        title_box = (x + 2, y + 2, x + card_w - 2, y + title_h)
        draw.rectangle(title_box, fill="#f5f5f5")

        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = x + (card_w - text_w) / 2
        text_y = y + (title_h - text_h) / 2 - 3
        draw.text((text_x, text_y), title, fill="#111111", font=title_font)

        panel_image = Image.open(path).convert("RGB")
        fitted = fit_cover(panel_image, (card_w - 8, card_h - title_h - 8))
        canvas.paste(fitted, (x + 4, y + title_h + 2))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT_PATH)
    print(f"Wrote showcase to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_showcase()
