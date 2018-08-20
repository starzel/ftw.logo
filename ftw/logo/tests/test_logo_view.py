from ftw.logo.testing import get_etag_value_for
from ftw.logo.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import os
from wand.exceptions import CorruptImageError
from wand.image import Image

source_path = os.path.join(os.path.dirname(__file__), 'fixtures')
custom = os.path.join(source_path, 'custom.svg')


class TestLogoView(FunctionalTestCase):

    @browsing
    def test_logo_view(self, browser):
        browser.visit(self.portal, view='@@logo/logo/BASE')
        self.assertEqual(200, browser.status_code)
        try:
            im = Image(blob=browser.contents, format='svg')
        except CorruptImageError:
            self.fail("Image is incorrect format - expected svg")

    @browsing
    def test_icon_view(self, browser):
        browser.visit(self.portal, view='@@logo/icon/BASE')
        self.assertEqual(200, browser.status_code)
        try:
            im = Image(blob=browser.contents, format='svg')
        except CorruptImageError:
            self.fail("Image is incorrect format - expected svg")

    @browsing
    def test_logo_scale(self, browser):
        browser.visit(self.portal, view='@@logo/logo/MOBILE_LOGO')
        self.assertEqual(200, browser.status_code)
        try:
            im = Image(blob=browser.contents, format='png')
        except CorruptImageError:
            self.fail("Image is incorrect format - expected png")
        self.assertEqual(50, im.height)

    @browsing
    def test_icon_scale(self, browser):
        browser.visit(self.portal, view='@@logo/icon/ANDROID_192X192')
        self.assertEqual(200, browser.status_code)
        try:
            im = Image(blob=browser.contents, format='png')
        except CorruptImageError:
            self.fail("Image is incorrect format - expected png")
        self.assertEqual(192, im.height)
        self.assertEqual(192, im.width)

    @browsing
    def test_not_found(self, browser):
        with browser.expect_http_error(code=404):
            browser.login().visit(self.portal, view='@@logo/logo/not_found')

        with browser.expect_http_error(code=404):
            browser.login().visit(self.portal, view='@@logo/not_found')

    def test_etag_value_invalidates(self):
        before = get_etag_value_for(self.portal, self.request)
        self.layer['load_zcml_string']('''
        <configure
            xmlns:logo="https://namespaces.4teamwork.ch/ftw.logo"
            i18n_domain="my.package"
            package="ftw.logo.tests">
            <logo:logo base="{}" />
        </configure>
        '''.format(custom))
        after = get_etag_value_for(self.portal, self.request)

        self.assertNotEqual(
            before,
            after)
