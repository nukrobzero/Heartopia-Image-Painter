from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image, ImageFilter, ImageEnhance


RGB = Tuple[int, int, int]


@dataclass
class PixelGrid:
    w: int
    h: int
    pixels: List[RGB]  # row-major

    def get(self, x: int, y: int) -> RGB:
        return self.pixels[y * self.w + x]


def load_and_resize_to_grid(path: str, w: int, h: int, sharpen: str = "none") -> PixelGrid:
    """Load and resize image to grid.
    
    Args:
        path: Image file path
        w: Target width
        h: Target height
        sharpen: Sharpening preset - "none", "mild", or "strong"
    """
    img = Image.open(path).convert("RGBA")

    # Composite alpha over white, so transparent areas become white.
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(bg, img)

    img = img.convert("RGB")
    img = img.resize((w, h), resample=Image.Resampling.LANCZOS)
    
    # Apply sharpening if requested
    try:
        if sharpen.lower() == "mild":
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)  # Mild sharpening
        elif sharpen.lower() == "strong":
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)  # Strong sharpening
        # "none" or other values: no sharpening
    except Exception:
        # If sharpening fails, continue without it
        pass
    
    pixels = list(img.getdata())
    return PixelGrid(w=w, h=h, pixels=[(int(r), int(g), int(b)) for (r, g, b) in pixels])
