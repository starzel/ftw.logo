from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from zope.interface import implements


class AbstractConfig(object):

    def __init__(self, base):
        self.base = base
        self.scales = {}

    def add_scale(self, name, scale):
        self.scales[name] = scale

    def get_scale(self, name):
        return self.scales[name]


class LogoConfig(AbstractConfig):
    """Logo config entry.
    """

    implements(ILogoConfig)


class IconConfig(AbstractConfig):
    """Icon config entry.
    """

    implements(IIconConfig)
