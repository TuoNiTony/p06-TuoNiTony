from io import BytesIO
import os

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

SOURCE = os.path.join(
    os.path.dirname(__file__), "..", "course", "images", "sticker.gif"
)


def resize_gif_through_pillow(width, height):
    with open(SOURCE, "rb") as source_file:
        source_bytes = source_file.read()

    config = Config(PILLOW_PRESERVE_INDEXED_MODE=True)
    context = Context(config=config)
    engine = Engine(context)
    engine.load(source_bytes, ".gif")
    engine.resize(width, height)
    return engine.read(".gif")


def test_resized_gif_keeps_transparent_background():
    source = Image.open(SOURCE).convert("RGBA")
    # The corner of the sticker is transparent in the source.
    assert source.getpixel((0, 0))[3] == 0

    output_bytes = resize_gif_through_pillow(240, 160)
    output = Image.open(BytesIO(output_bytes))

    assert "transparency" in output.info

    output_rgba = output.convert("RGBA")
    assert output_rgba.getpixel((0, 0))[3] == 0
