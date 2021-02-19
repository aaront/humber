import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import List

from PIL import Image

from . import Engine


@dataclass
class ImageOutputMeta:
    path: Path
    format: str
    width: int


@dataclass
class ImageMeta:
    original_path: Path
    outputs: List[ImageOutputMeta]


class ImageEngine(Engine):
    widths: List[int]
    formats: List[str]
    output_path: Path

    def __init__(
        self,
        widths: List[int] = [300, 1000],
        formats: List[str] = ["webp", "jpg"],
        output_path=None,
    ) -> None:
        super().__init__()
        self.widths = widths
        self.formats = formats
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
            source_image.resize((width, height))
            filename, _ = os.path.splitext(os.path.basename(source_image.filename))
            for format in self.formats:
                output_path = self.output_path / f"{filename}.{width}w.{format}"
                source_image.save(output_path)
                image_outputs.append(ImageOutputMeta(output_path, format, width))
        return ImageMeta(fp, image_outputs)

    def generate_html(self, fp: Path, template: str = None) -> str:
        pass
