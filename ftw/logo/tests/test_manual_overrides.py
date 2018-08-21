from ftw.builder import Builder
from ftw.builder import create
from ftw.logo.manual_override import OVERRIDES_FIXED_ID
from ftw.logo.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import os
from plone.app.layout.navigation.interfaces import INavigationRoot
import transaction
from wand.color import Color
from wand.exceptions import CorruptImageError
from wand.image import Image
from zope.interface import alsoProvides


source_path = os.path.join(os.path.dirname(__file__), 'fixtures')
red_svg = os.path.join(source_path, 'red.svg')
green_png = os.path.join(source_path, 'green.png')


class TestManualOverrides(FunctionalTestCase):

    @browsing
    def test_permission_for_overrides_form(self, browser):

        # test editor user can't use add form
        self.grant('Editor')
        with browser.expect_unauthorized():
            browser.login().visit(self.portal, view='@@logo-and-icon-overrides')

        # test site admin CAN use the overrides form
        self.grant('Site Administrator')
        browser.visit(self.portal, view='@@logo-and-icon-overrides')
        self.assertEqual(200, browser.status_code)

        # test editor user can't view the content type
        self.grant('Editor')
        with browser.expect_unauthorized():
            browser.login().visit(self.portal[OVERRIDES_FIXED_ID])

        # test editor user can't view the content type
        self.grant('Site Administrator')
        browser.login().visit(self.portal[OVERRIDES_FIXED_ID])
        self.assertEqual(200, browser.status_code)


    @browsing
    def test_addable_only_on_navroots(self, browser):
        self.grant('Site Administrator')
        browser.login()
        folder = create(Builder('folder'))
        with browser.expect_http_error(code=404):
            browser.login().visit(folder, view='@@logo-and-icon-overrides')

        # If we make the folder a navroot then we should be able to access the form on it
        # FIXME - 500 from ComponentLookupError in LogoViewletETagValue
        #alsoProvides(self.portal['folder'], INavigationRoot)
        #transaction.commit()
        #browser.visit(folder, view='@@logo-and-icon-overrides')
        #self.assertEqual(200, browser.status_code)


    def verify_correct_image(self, browser, view, expected_format, expected_colour=None):
        # We logout to test images are *publicly* visible
        browser.logout()
        browser.visit(self.portal, view=view)
        self.assertEqual(200, browser.status_code)
        try:
            im = Image(blob=browser.contents, format=expected_format)
        except CorruptImageError:
            self.fail("Image is incorrect format - expected {}".format(expected_format))
        if (expected_colour):
            # Determine the source (SVG, PNG) by using the colour
            # Test that 90% of image is expected_colour
            num_pixels = im.height * im.width
            self.assertGreater(im.histogram[Color(expected_colour)], num_pixels * 0.9)
        return im


    @browsing
    def test_overrides(self, browser):
        # test adding overrides
        self.grant('Site Administrator')
        browser.login().visit(self.portal, view='@@logo-and-icon-overrides')
        self.assertEqual(200, browser.status_code)
        with open(red_svg) as svg_file:
            browser.fill({'SVG base logo': svg_file}).submit()

        # Check SVG image is set
        img = self.verify_correct_image(browser, '@@logo/logo/BASE', 'svg', 'red')
        # Check conversion to PNG
        img = self.verify_correct_image(browser, '@@logo/logo/MOBILE_LOGO', 'png', 'red')
        self.assertEqual(50, img.height)
        # Check ZCML 'bypass'
        img = self.verify_correct_image(browser, '@@logo/z/logo/MOBILE_LOGO', 'png')
        # TODO verify base SVG is shown
        # TODO verify icons are unchanged

        # Test PNG override
        browser.login().visit(self.portal, view='@@logo-and-icon-overrides')
        with open(green_png) as png_file:
            browser.fill({'Mobile logo (PNG)': png_file}).submit()
        img = self.verify_correct_image(browser, '@@logo/logo/MOBILE_LOGO', 'png', '#0f0')
        # Note dimensions of a PNG override are not enforced
        # Check ZCML 'bypass'
        img = self.verify_correct_image(browser, '@@logo/z/logo/MOBILE_LOGO', 'png')
        # TODO verify base SVG is shown

        # TODO test icons similar to above



    @browsing
    def test_form_validation(self, browser):
        self.grant('Site Administrator')
        browser.login().visit(self.portal, view='@@logo-and-icon-overrides')
        with open(green_png) as png_file:
            browser.fill({'SVG base logo': png_file}).submit()
        self.assertIn('This image must be a SVG file (image/png supplied)', browser.contents)

        browser.login().visit(self.portal, view='@@logo-and-icon-overrides')
        with open(red_svg) as svg_file:
            browser.fill({'Apple touch icon': svg_file}).submit()
        self.assertIn('This image must be a PNG file (image/svg+xml supplied)', browser.contents)
