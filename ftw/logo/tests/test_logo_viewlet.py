from ftw.logo.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestLogoViewlet(FunctionalTestCase):

    @browsing
    def test_logo_tag(self, browser):
        browser.login().visit(self.portal)

        self.assertEqual(
            map(lambda x: x.attrib['href'], browser.css('.portal-logo')),
            ['http://nohost/plone'],
        )

        self.assertEqual(
            map(lambda x: x.attrib['src'], browser.css('.portal-logo > img')),
            ['http://nohost/plone/@@logo/logo/BASE'],
        )
