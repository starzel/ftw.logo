from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from zope.interface import implements
from hashlib import sha256


class AbstractConfig(object):

    def __init__(self, base):
        self.base = base
        self.cachekey = self.get_cachekey_from_path(self.base)
        self.scales = {}

    def add_scale(self, name, scale):
        self.scales[name] = scale

    def get_scale(self, name):
        return self.scales[name]

    def get_cachekey_from_path(self, path):
        cachekey = sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                cachekey.update(chunk)
        return cachekey.hexdigest()


class LogoConfig(AbstractConfig):
    """Logo config entry.
    """

    implements(ILogoConfig)


class IconConfig(AbstractConfig):
    """Icon config entry.
    """

    implements(IIconConfig)
