import os.path
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

import pillow_avif  # noqa: F401
from jinja2 import Markup
from PIL import Image as _Image

from jinja2 import Environment, FileSystemLoader

_IMAGE_QUALITIES = {
    "default": 80,
    "avif": 70,
}

_IMAGE_MIMETYPES = {
    "avif": "image/avif",
    "webp": "image/webp",
    "jpg": "image/jpeg",
}


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
    ext: str
    url: str

    def __init__(self, path: Path, url: str) -> None:
        if not path or not path.exists:
            raise TypeError("Image path was not provided")
        if not path.exists():
            raise ValueError(f"Image path '{path}' does not exist")
        self._image = _Image.open(path)
        self.filename, self.ext = os.path.splitext(
            os.path.basename(self._image.filename)
        )
        self.url = url

    def scale_width(self, max_width: int) -> _Image:
        source_w, source_h = self._image.size
        w_ratio = max_width / float(source_w)
        max_height = int(source_h * w_ratio)
        return self._image.resize((max_width, max_height))


def generate_srcsets(
    image: Image,
    output_path: Path,
    format: str,
    widths: List[int] = [300, 1000],
    quality: int = None,
):
    srcsets: List[str] = []
    for width in sorted(widths, reverse=True):
        scaled_image = image.scale_width(width)
        output_filename = f"{image.filename}.{width}w.{format}"
        output_file = output_path / output_filename
        image_quality = quality or _IMAGE_QUALITIES.get(
            format, _IMAGE_QUALITIES.get("default")
        )
        scaled_image.save(
            output_file,
            quality=image_quality,
            speed=0,  # AVIF
            method=6,  # WebP
            **_get_avif_qmin_max(image_quality),
        )
        srcsets.append(f"{image.url}/{output_filename} {width}w")
    sizes = "(max-width: 608px) 100vw, 608px"
    image_type = _IMAGE_MIMETYPES[format]
    return Markup(f'sizes="{sizes}" srcset="{", ".join(srcsets)}" type="{image_type}"')


env = Environment(
    loader=FileSystemLoader(Path(__file__).resolve().parent / "templates"),
    enable_async=True,
)
env.filters["generate_srcsets"] = generate_srcsets


async def render_image(
    image: Image, output_path: Path, formats: List[str], widths: List[int]
):
    template = env.get_template("image.html")
    return await template.render_async(
        image=image, output_path=output_path, formats=formats, widths=widths
    )


def _get_avif_qmin_max(quality: Optional[int]) -> Dict[str, int]:
    if not quality:
        return {}
    return {
        "qmin": max(0, min(64 - quality, 63)),
        "qmax": max(0, min(100 - quality, 63)),
    }
