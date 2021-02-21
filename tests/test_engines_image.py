from pathlib import Path

from humber.engines.image import ImageEngine


def test_generate_images(tmp_path: Path):
    input_file = Path(__file__).resolve().parent / "images" / "IMGP8501.jpg"
    ImageEngine(output_path=tmp_path).generate(input_file)
    files = list(tmp_path.iterdir())
    assert len(files) == 6
