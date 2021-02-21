import os.path
from pathlib import Path
from typing import Dict, List, TypedDict

import pillow_avif  # noqa: F401
from PIL import Image

from . import Engine

DEFAULT_IMAGE_QUALITY = 80


class ImageOutputMeta(TypedDict):
    path: Path
    format: str
    width: int


class ImageMeta(TypedDict):
    original_path: Path
    outputs: List[ImageOutputMeta]


class ImageEngine(Engine):
    widths: List[int]
    formats: List[str]
    qualities: Dict[str, int]
    output_path: Path

    def __init__(
        self,
        widths: List[int] = [300, 1000],
        formats: List[str] = ["webp", "avif", "jpg"],
        qualities: Dict[str, int] = {"avif": 70},
        output_path=None,
    ) -> None:
        super().__init__()
        self.widths = widths
        self.formats = formats
        self.qualities = qualities
        self.output_path = output_path

    def generate(self, fp: Path) -> ImageMeta:
        if not self.output_path:
            raise ValueError("output_path not provided")
        source_image = Image.open(fp)
        source_w, source_h = source_image.size
        image_outputs: List[ImageOutputMeta] = []
        for width in self.widths:
            w_ratio = width / float(source_w)
            height = int(source_h * w_ratio)
            scaled_image = source_image.resize((width, height))
            filename, _ = os.path.splitext(os.path.basename(source_image.filename))
            for format in self.formats:
                output_path = self.output_path / f"{filename}.{width}w.{format}"
                quality = self.qualities.get(format) or DEFAULT_IMAGE_QUALITY
                scaled_image.save(
                    output_path,
                    quality=quality,
                    speed=0,  # AVIF
                    method=6,  # WebP
                    **_get_avif_qmin_max(quality),
                )
                image_outputs.append(
                    ImageOutputMeta(path=output_path, format=format, width=width)
                )
        return ImageMeta(original_path=fp, outputs=image_outputs)

    def generate_html(self, fp: Path, template: str = None) -> str:
        pass


def _get_avif_qmin_max(quality: int) -> Dict[str, int]:
    return {
        "qmin": max(0, min(64 - quality, 63)),
        "qmax": max(0, min(100 - quality, 63)),
    }
