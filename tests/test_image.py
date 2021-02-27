import pytest

from pathlib import Path

from humber.image import Image, generate_srcsets, render_image


def test_image():
    with pytest.raises(TypeError) as typeerror:
        Image(None, "")
    assert "not provided" in str(typeerror.value)
    with pytest.raises(ValueError) as valueerror:
        Image(Path(__file__).resolve().parent / "images" / "doesntexist.jpg", "")
    assert "does not exist" in str(valueerror.value)


def test_generate_srcsets(tmp_path: Path):
    input_file = Path(__file__).resolve().parent / "images" / "IMGP8501.jpg"
    image = Image(input_file, "posts/2021")
    srcsets = generate_srcsets(image, tmp_path, format="webp", widths=[150, 300])
    assert (
        srcsets
        == 'sizes="(max-width: 608px) 100vw, 608px" srcset="posts/2021/IMGP8501.300w.webp 300w, posts/2021/IMGP8501'
        '.150w.webp 150w" type="image/webp"'
    )


@pytest.mark.asyncio
async def test_render_image(tmp_path: Path):
    input_file = Path(__file__).resolve().parent / "images" / "IMGP8501.jpg"
    image = Image(input_file, "posts/2021")
    rendered_html = await render_image(
        image=image,
        output_path=tmp_path,
        formats=["avif", "webp", "jpg"],
        widths=[150, 300],
    )
    assert (
        'srcset="posts/2021/IMGP8501.300w.avif 300w, posts/2021/IMGP8501.150w.avif 150w" type="image/avif"'
        in rendered_html
    )
    assert (
        'srcset="posts/2021/IMGP8501.300w.avif 300w, posts/2021/IMGP8501.150w.avif 150w" type="image/avif"'
        in rendered_html
    )
    assert (
        'srcset="posts/2021/IMGP8501.300w.avif 300w, posts/2021/IMGP8501.150w.avif 150w" type="image/avif"'
        in rendered_html
    )
    assert (
        'src="posts/2021/IMGP8501.jpg" style="background-size: cover; background-image: none;" decoding="async" '
        'loading="lazy"' in rendered_html
    )
