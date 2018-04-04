from ftw.logo.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestLogoView(FunctionalTestCase):

    @browsing
    def test_logo_view(self, browser):
        browser.login().visit(self.portal, view='@@logo/logo/base')
        self.assertEqual(200, browser.status_code)

    @browsing
    def test_icon_view(self, browser):
        browser.login().visit(self.portal, view='@@logo/logo/base')
        self.assertEqual(200, browser.status_code)

    @browsing
    def test_not_found(self, browser):
        with browser.expect_http_error(code=404):
            browser.login().visit(self.portal, view='@@logo/logo/not_found')

        with browser.expect_http_error(code=404):
            browser.login().visit(self.portal, view='@@logo/not_found')
