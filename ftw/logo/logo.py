from ftw.logo.interfaces import ILogo
from ftw.logo.interfaces import ILogoConfig
from ftw.logo.interfaces import IIconConfig
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getMultiAdapter


@implementer(ILogo)
@adapter(IPloneSiteRoot, Interface)
class Logo(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_config(self, config_type):
        return getMultiAdapter((self.context, self.request), config_type)

    def get_logo_config(self):
        return getMultiAdapter((self.context, self.request), ILogoConfig)

    def get_icon_config(self):
        return getMultiAdapter((self.context, self.request), IIconConfig)
