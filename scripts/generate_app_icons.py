"""Resize app-icon-cooler-sync master into PWA and Android mipmap assets."""
from pathlib import Path

from PIL import Image

SRC = Path(__file__).resolve().parents[1] / "static" / "icons" / "app-icon-cooler-sync.png"
# Fallback: Cursor-generated asset before copy into repo
CURSOR_SRC = Path(
    r"C:\Users\IT\.cursor\projects\d-projects-rider-app\assets\app-icon-cooler-sync.png"
)
REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    src = SRC if SRC.is_file() else CURSOR_SRC
    if not src.is_file():
        raise SystemExit(f"Source icon not found: {src}")

    img = Image.open(src).convert("RGBA")
    pwa_dir = REPO / "static" / "icons"
    pwa_dir.mkdir(parents=True, exist_ok=True)

    for size, name in [(192, "icon-192.png"), (512, "icon-512.png")]:
        out = pwa_dir / name
        img.resize((size, size), Image.Resampling.LANCZOS).save(out, optimize=True)
        print("wrote", out)

    master = pwa_dir / "app-icon-cooler-sync.png"
    if not master.is_file() or src != master:
        img.resize((1024, 1024), Image.Resampling.LANCZOS).save(master, optimize=True)
        print("wrote", master)

    densities = [
        ("mipmap-mdpi", 48, 108),
        ("mipmap-hdpi", 72, 162),
        ("mipmap-xhdpi", 96, 216),
        ("mipmap-xxhdpi", 144, 324),
        ("mipmap-xxxhdpi", 192, 432),
    ]
    res = REPO / "android" / "app" / "src" / "main" / "res"
    for folder, launcher_px, fg_px in densities:
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


if __name__ == "__main__":
    main()
