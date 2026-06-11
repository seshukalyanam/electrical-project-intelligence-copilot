from __future__ import annotations

from pathlib import Path


def ocr_image(path: Path) -> str:
    try:
        import pytesseract
        from PIL import Image

        return pytesseract.image_to_string(Image.open(path))
    except Exception:
        return ""
