from ftw.logo.image import Image
from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from textwrap import wrap
from zope.interface import implements
from hashlib import sha256

class AbstractConfig(object):

    def __init__(self, base):
        self.base = Image(filename=base)
        self.cachekey = self.get_cachekey_from_blob(self.base.make_blob())
        self.scales = {}

    def add_scale(self, name, scale):
        self.scales[name] = scale

    def get_scale(self, name):
        return self.scales[name]

    def get_cachekey_from_blob(self, blob):
        cachekey = sha256()
        for chunk in wrap(blob, 4096):
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

class AbstractConfigOverride(AbstractConfig):

    def __init__(self, blobImage):
        self.base = Image(blob=blobImage.data, format='svg')
        self.cachekey = self.get_cachekey_from_blob(blobImage.data)
        self.scales = {}

class LogoConfigOverride(AbstractConfigOverride):
    """Logo config (TTW) overrides.
    """

    implements(ILogoConfig)


class IconConfigOverride(AbstractConfigOverride):
    """Icon config (TTW) overrides.
    """

    implements(IIconConfig)

