import os
from io import BytesIO

from PIL import Image
from tornado.testing import gen_test

from tests.handlers.test_base_handler import BaseImagingTestCase
from thumbor.config import Config
from thumbor.context import Context, ServerParameters
from thumbor.importer import Importer

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "course", "images")
)


class ExtremeAspectTestCase(BaseImagingTestCase):
    def get_context(self):
        cfg = Config(SECURITY_KEY="ACME-SEC")
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = ROOT
        importer = Importer(cfg)
        importer.import_modules()
        server = ServerParameters(
            8889, "localhost", "thumbor.conf", None, "info", None
        )
        return Context(server, cfg, importer)

    @gen_test
    def test_extreme_aspect_ratio_keeps_size_and_alpha(self):
        response = yield self.async_fetch("/unsafe/800x20/rainbow.png")
        self.assertEqual(response.code, 200)
        image = Image.open(BytesIO(response.body)).convert("RGBA")
        self.assertEqual(image.size, (800, 20))
        self.assertGreater(image.getchannel("A").getextrema()[1], 0)

    @gen_test
    def test_fit_in_1x1_returns_1x1(self):
        response = yield self.async_fetch("/unsafe/fit-in/1x1/940x2.png")
        self.assertEqual(response.code, 200)
        image = Image.open(BytesIO(response.body))
        self.assertEqual(image.size, (1, 1))

    @gen_test
    def test_fit_in_100x0_returns_100x1(self):
        response = yield self.async_fetch("/unsafe/fit-in/100x0/940x2.png")
        self.assertEqual(response.code, 200)
        image = Image.open(BytesIO(response.body))
        self.assertEqual(image.size, (100, 1))
