from unittest2 import TestCase
from ftw.testing import freeze
from ftw.logo.converter import convert
from datetime import datetime
import os


source = os.path.join(os.path.dirname(__file__), 'fixtures/logo.svg')


class TestConverter(TestCase):

    def assertImage(self, img, width, height, format=None, blob=None):
        self.assertEqual(img.width, width)
        self.assertEqual(img.height, height)
        if format:
            self.assertEqual(img.format.lower(), format.lower())
        if blob:
            self.assertEqual(img.make_blob(), blob)

    def test_rejects_unsupported_types(self):
        with self.assertRaises(Exception) as context:
            convert(source, 'UNKNOWN')

        self.assertTrue('scale: UNKNOWN is not supported' in context.exception)

    def test_converts_svg_base(self):
        self.assertImage(
            convert(source, 'BASE'), 1, 1, 'svg',
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg width="1px" height="1px" viewBox="0 0 1 1" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
            '    <g id="logo"></g>\n'
            '</svg>\n'
        )

    def test_converts_png_fixed_size(self):
        self.assertImage(
            convert(source, 'APPLE_TOUCH_ICON'), 180, 180, 'png')

    def test_converts_png_fixed_aspect_ratio(self):
        self.assertImage(
            convert(source, 'LOGO'), 80, 80, 'png')

    def test_converts_multipart_images(self):
        img = convert(source, 'FAVICON')
        self.assertEqual(len(img.sequence), 3,
                         'Should contain three subimages in the sequence')

        self.assertImage(
            img.sequence[0], 16, 16)

        self.assertImage(
            img.sequence[1], 32, 32)

        self.assertImage(
            img.sequence[2], 48, 48)

        img.close()
