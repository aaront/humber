import pytest

from pathlib import Path

from humber.image import ResponsiveImage


def test_image():
    with pytest.raises(TypeError) as typeerror:
        ResponsiveImage(None)
    assert "not provided" in str(typeerror.value)
    with pytest.raises(ValueError) as valueerror:
        ResponsiveImage(Path(__file__).resolve().parent / "images" / "doesntexist.jpg")
    assert "does not exist" in str(valueerror.value)


def test_generate(tmp_path: Path):
    input_file = Path(__file__).resolve().parent / "images" / "IMGP8501.jpg"
    ResponsiveImage(input_file, widths=[150, 300]).generate(output_path=tmp_path)
    files = list(tmp_path.iterdir())
    assert len(files) == 6
