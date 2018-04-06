from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from ftw.logo.testing import META_ZCML
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.interface.verify import verifyObject
from zope.interface import Interface
from zope.interface import implementer


class IDummyLayer(Interface):
    pass


@implementer(IDummyLayer)
class DummyRequest(object):
    pass


class TestZCML(TestCase):
    layer = META_ZCML

    def test_logo_component(self):
        self.load_zcml(
            '<logo:logo base="/base.svg" />')
        registry = getMultiAdapter((None, None), ILogoConfig)
        self.assertEqual('/base.svg', registry.base)
        verifyObject(ILogoConfig, registry)

    def test_logo_component_is_overwriteable(self):
        self.load_zcml(
            '<logo:logo base="/default.svg" />',
            '<logo:logo base="/custom.svg"',
            '  layer="ftw.logo.tests.test_zcml.IDummyLayer" />')
        registry = getMultiAdapter((object(), DummyRequest()), ILogoConfig)
        self.assertEqual('/custom.svg', registry.base)
        verifyObject(ILogoConfig, registry)

    def test_icon_component(self):
        self.load_zcml(
            '<logo:icon base="/base.svg" />')
        registry = getMultiAdapter((None, None), IIconConfig)
        self.assertEqual('/base.svg', registry.base)
        verifyObject(IIconConfig, registry)

    def test_icon_component_is_overwriteable(self):
        self.load_zcml(
            '<logo:icon base="/default.svg" />',
            '<logo:icon base="/custom.svg"',
            '  layer="ftw.logo.tests.test_zcml.IDummyLayer" />')
        registry = getMultiAdapter((object(), DummyRequest()), IIconConfig)
        self.assertEqual('/custom.svg', registry.base)
        verifyObject(IIconConfig, registry)

    def load_zcml(self, *lines):
        self.layer.load_zcml_string('\n'.join((
            '<configure ',
            '    xmlns:logo="https://namespaces.4teamwork.ch/ftw.logo"',
            '    i18n_domain="my.package"',
            '    package="ftw.logo.tests"''>',
        ) + lines + (
            '</configure>',
        )))
