import os.path
from pathlib import Path
from typing import Dict, List, TypedDict

import pillow_avif  # noqa: F401
from PIL import Image as _Image

DEFAULT_IMAGE_QUALITY = 80


class ImageOutputMeta(TypedDict):
    path: Path
    format: str
    width: int


class ImageMeta(TypedDict):
    original_path: Path
    outputs: List[ImageOutputMeta]


class Image:
    _image: _Image
    filename: str

    def __init__(self, path: Path) -> None:
        if not path or not path.exists:
            raise TypeError("Image path was not provided")
        if not path.exists():
            raise ValueError(f"Image path '{path}' does not exist")
        self._image = _Image.open(path)
        self.filename, _ = os.path.splitext(os.path.basename(self._image.filename))

    def scale_width(self, max_width: int) -> _Image:
        source_w, source_h = self._image.size
        w_ratio = max_width / float(source_w)
        max_height = int(source_h * w_ratio)
        return self._image.resize((max_width, max_height))


class ResponsiveImage(Image):
    widths: List[int]
    formats: List[str]
    qualities: Dict[str, int]

    def __init__(
        self,
        path: Path,
        widths: List[int] = [300, 1000],
        formats: List[str] = ["webp", "avif", "jpg"],
        qualities: Dict[str, int] = {"avif": 70},
    ) -> None:
        super().__init__(path)
        self.widths = widths
        self.formats = formats
        self.qualities = qualities

    def generate(self, output_path: Path):
        image_outputs: List[ImageOutputMeta] = []
        for width in self.widths:
            scaled_image = self.scale_width(width)
            for format in self.formats:
                output_file = output_path / f"{self.filename}.{width}w.{format}"
                quality = self.qualities.get(format) or DEFAULT_IMAGE_QUALITY
                scaled_image.save(
                    output_file,
                    quality=quality,
                    speed=0,  # AVIF
                    method=6,  # WebP
                    **_get_avif_qmin_max(quality),
                )
                image_outputs.append(
                    ImageOutputMeta(path=output_file, format=format, width=width)
                )
        return ImageMeta(original_path=output_file, outputs=image_outputs)


def _get_avif_qmin_max(quality: int) -> Dict[str, int]:
    return {
        "qmin": max(0, min(64 - quality, 63)),
        "qmax": max(0, min(100 - quality, 63)),
    }
