from ftw.logo.interfaces import ILogo
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
