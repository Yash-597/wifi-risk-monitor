from __future__ import annotations
from PIL import Image, ImageDraw
from core.models import RiskLevel


def build_icon(level: RiskLevel) -> Image.Image:
    color = _color_for_level(level)
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 56, 56), radius=10, fill=color)
    draw.arc((18, 24, 46, 52), 200, 340, fill="white", width=5)
    draw.arc((24, 32, 40, 52), 205, 335, fill="white", width=5)
    draw.ellipse((29, 45, 35, 51), fill="white")
    return image


def _color_for_level(level: RiskLevel) -> tuple[int, int, int, int]:
    if level == RiskLevel.RISKY:
        return (210, 58, 58, 255)
    if level == RiskLevel.PROTECTED:
        return (32, 126, 168, 255)
    if level == RiskLevel.PAUSED:
        return (120, 126, 138, 255)
    if level == RiskLevel.UNKNOWN:
        return (190, 139, 32, 255)
    if level == RiskLevel.TRUSTED:
        return (42, 130, 218, 255)
    return (40, 154, 96, 255)
