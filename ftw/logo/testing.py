from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class MetaZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(MetaZCMLLayer, self).setUp()
        import ftw.logo
        self.load_zcml_file('meta.zcml', ftw.logo)


META_ZCML = MetaZCMLLayer()


class LogoLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.logo')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.logo:default')


LOGO_FIXTURE = LogoLayer()
LOGO_FUNCTIONAL = FunctionalTesting(
    bases=(LOGO_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.logo:functional")
