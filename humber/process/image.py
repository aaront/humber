import os.path
from pathlib import Path
from typing import List

from PIL import Image


def create_images(
    input_path: Path,
    output_dir: Path,
    widths: List[int] = [300, 1000],
    formats: List[str] = ["webp", "jpg"],
):
    source_image = Image.open(input_path)
    source_w, source_h = source_image.size
    for width in widths:
        w_ratio = width / float(source_w)
        height = int(source_h * w_ratio)
        source_image.resize((width, height))
        filename, _ = os.path.splitext(os.path.basename(source_image.filename))
        for format in formats:
            output_filename = f"{filename}.{width}w.{format}"
            source_image.save(os.path.join(output_dir, output_filename))
