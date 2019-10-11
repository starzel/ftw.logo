from unittest2 import TestCase
from ftw.logo.logoconfig import LogoConfig
from ftw.logo.logoconfig import IconConfig
import os


source = os.path.join(os.path.dirname(__file__), 'fixtures/logo.svg')
img_source = os.path.join(os.path.dirname(__file__), 'fixtures/logo.png')


class TestCollecter(TestCase):

    def assertImage(self, img, width, height, format=None):
        self.assertEqual(img['width'], width)
        self.assertEqual(img['height'], height)
        if format:
            self.assertEqual(img['format'].lower(), format.lower())

    def test_all_logos_are_collected(self):
        component = LogoConfig(logo=source)

        self.assertEqual(len(component.scales), 2, 'Should store two scales')
        self.assertImage(component.get_scale('LOGO'), 1, 1, 'svg')
        self.assertIsNone(component.get_scale('MOBILE_LOGO'))

    def test_all_icons_are_collected(self):
        component = IconConfig(base=source)

        self.assertEqual(len(component.scales), 8, 'Should store eight scales')
        self.assertImage(component.get_scale('BASE'), 1, 1, 'svg')
        self.assertImage(component.get_scale('APPLE_TOUCH_ICON'), 180, 180, 'png')
        self.assertImage(component.get_scale('FAVICON_32X32'), 32, 32, 'png')
        self.assertImage(component.get_scale('FAVICON_16X16'), 16, 16, 'png')
        self.assertImage(component.get_scale('MSTILE_150X150'), 150, 150, 'png')
        self.assertImage(component.get_scale('ANDROID_192X192'), 192, 192, 'png')
        self.assertImage(component.get_scale('ANDROID_512X512'), 512, 512, 'png')
        self.assertImage(component.get_scale('FAVICON'), 16, 16, 'ico')

    def test_add_specific_mobile_logo_as_config(self):
        component = LogoConfig(logo=source, mobile=img_source)

        self.assertEqual(len(component.scales), 2, 'Should store one scales')
        self.assertImage(component.get_scale('LOGO'), 1, 1, 'svg')

        self.assertImage(component.get_scale('MOBILE_LOGO'), 200, 21, 'png')
