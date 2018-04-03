from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from zope.interface import implements


class LogoConfig(object):
    """Logo config entry.
    """

    implements(ILogoConfig)

    def __init__(self, base):
        self.base = base


class IconConfig(object):
    """Icon config entry.
    """

    implements(IIconConfig)

    def __init__(self, base):
        self.base = base
