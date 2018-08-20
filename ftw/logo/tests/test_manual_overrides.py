from ftw.builder import Builder
from ftw.builder import create
from ftw.logo.manual_override import OVERRIDES_FIXED_ID
from ftw.logo.tests import FunctionalTestCase
from ftw.testbrowser import browsing

class TestManualOverrides(FunctionalTestCase):
    #layer = LOGO_FUNCTIONAL


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


    @browsing
    def test_overrides(self, browser):
        # TODO test adding overrides
        self.grant('Site Administrator')
        browser.login().visit(self.portal, view='@@logo-and-icon-overrides')
        self.assertEqual(200, browser.status_code)
        # TODO conversion to PNG
        # Test view of PNG
        # TODO test fallback if overrides not set
        # TODO test overrides *publicly* visible too
        pass

    def test_form_validation(self):
        pass

    def test_zcml_bypass(self):
        pass
