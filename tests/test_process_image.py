from pathlib import Path

from humber.process.image import create_images


def test_output_images(tmp_path: Path):
    input_file = Path(__file__).resolve().parent / "images" / "IMGP8501.jpg"
    create_images(input_file, output_dir=tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 4
