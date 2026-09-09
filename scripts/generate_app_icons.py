"""Resize a master app icon into PWA and/or Android mipmap assets."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SRC = REPO / "static" / "icons" / "app-icon-cooler-sync.png"
DENSITIES = [
    ("mipmap-mdpi", 48, 108),
    ("mipmap-hdpi", 72, 162),
    ("mipmap-xhdpi", 96, 216),
    ("mipmap-xxhdpi", 144, 324),
    ("mipmap-xxxhdpi", 192, 432),
]


def write_mipmaps(img: Image.Image, res: Path) -> None:
    for folder, launcher_px, fg_px in DENSITIES:
        d = res / folder
        d.mkdir(parents=True, exist_ok=True)
        launcher = img.resize((launcher_px, launcher_px), Image.Resampling.LANCZOS)
        fg = img.resize((fg_px, fg_px), Image.Resampling.LANCZOS)
        for name, im in [
            ("ic_launcher.png", launcher),
            ("ic_launcher_round.png", launcher),
            ("ic_launcher_foreground.png", fg),
        ]:
            path = d / name
            im.save(path, optimize=True)
            print("wrote", path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument(
        "--res",
        type=Path,
        default=REPO / "android" / "app" / "src" / "main" / "res",
    )
    parser.add_argument("--skip-pwa", action="store_true")
    parser.add_argument("--pwa-master-name", default="app-icon-cooler-sync.png")
    args = parser.parse_args()

    src = args.src
    if not src.is_file():
        raise SystemExit(f"Source icon not found: {src}")

    img = Image.open(src).convert("RGBA")
    if not args.skip_pwa:
        pwa_dir = REPO / "static" / "icons"
        pwa_dir.mkdir(parents=True, exist_ok=True)
        for size, name in [(192, "icon-192.png"), (512, "icon-512.png")]:
            out = pwa_dir / name
            img.resize((size, size), Image.Resampling.LANCZOS).save(out, optimize=True)
            print("wrote", out)
        master = pwa_dir / args.pwa_master_name
        img.resize((1024, 1024), Image.Resampling.LANCZOS).save(master, optimize=True)
        print("wrote", master)

    write_mipmaps(img, args.res)


if __name__ == "__main__":
    main()
