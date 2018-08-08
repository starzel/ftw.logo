from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from ftw.logo.testing import META_ZCML
from unittest2 import TestCase
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.verify import verifyObject
import os


source_path = os.path.join(os.path.dirname(__file__), 'fixtures')
logo = os.path.join(source_path, 'logo.svg')
icon = os.path.join(source_path, 'logo.svg')
custom = os.path.join(source_path, 'custom.svg')


class IDummyLayer(Interface):
    pass


@implementer(IDummyLayer)
class DummyRequest(object):
    pass


class TestZCML(TestCase):
    layer = META_ZCML

    def test_logo_component(self):
        self.load_zcml('<logo:logo base="{}" />'.format(logo))
        registry = getMultiAdapter((None, None), ILogoConfig)
        self.assertEqual(logo, registry.base.filename)
        verifyObject(ILogoConfig, registry)

    def test_logo_component_is_overwriteable(self):
        self.load_zcml(
            '<logo:logo base="{}" />'.format(logo),
            '<logo:logo base="{}"'.format(custom),
            '  layer="ftw.logo.tests.test_zcml.IDummyLayer" />')
        registry = getMultiAdapter((object(), DummyRequest()), ILogoConfig)
        self.assertEqual(custom, registry.base.filename)
        verifyObject(ILogoConfig, registry)

    def test_icon_component(self):
        self.load_zcml(
            '<logo:icon base="{}" />'.format(icon))
        registry = getMultiAdapter((None, None), IIconConfig)
        self.assertEqual(icon, registry.base.filename)
        verifyObject(IIconConfig, registry)

    def test_icon_component_is_overwriteable(self):
        self.load_zcml(
            '<logo:icon base="{}" />'.format(icon),
            '<logo:icon base="{}"'.format(custom),
            '  layer="ftw.logo.tests.test_zcml.IDummyLayer" />')
        registry = getMultiAdapter((object(), DummyRequest()), IIconConfig)
        self.assertEqual(custom, registry.base.filename)
        verifyObject(IIconConfig, registry)

    def load_zcml(self, *lines):
        self.layer.load_zcml_string('\n'.join((
            '<configure ',
            '    xmlns:logo="https://namespaces.4teamwork.ch/ftw.logo"',
            '    i18n_domain="my.package"',
            '    package="ftw.logo.tests">',
        ) + lines + (
            '</configure>',
        )))
