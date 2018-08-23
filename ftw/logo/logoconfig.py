from ftw.logo.converter import convert
from ftw.logo.converter import SCALES
from ftw.logo.image import Image
from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from textwrap import wrap
from zope.interface import implements
from hashlib import sha256

class AbstractConfig(object):

    def __init__(self, base):
        base_img = Image(filename=base)
        self.cachekey = self.get_cachekey_from_blob(base_img.make_blob())
        self.scales = {}
        self.collect_scales(base_img)

    def add_scale(self, name, scale):
        self.scales[name] = scale

    def collect_scales(self, base_img):
        raise NotImplemented()  # pragma: no cover

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

    def collect_scales(self, base_img):
        for scale in SCALES['LOGOS']:
            self.add_scale(scale, convert(base_img, scale))

class IconConfig(AbstractConfig):
    """Icon config entry.
    """

    implements(IIconConfig)

    def collect_scales(self, base_img):
        for scale in SCALES['ICONS']:
            self.add_scale(scale, convert(base_img, scale))

class AbstractConfigOverride(AbstractConfig):

    def __init__(self, blobImage):
        base_img = Image(blob=blobImage.data, format='svg')
        self.cachekey = self.get_cachekey_from_blob(blobImage.data)
        self.scales = {}
        self.collect_scales(base_img)

class LogoConfigOverride(AbstractConfigOverride):
    """Logo config (TTW) overrides.
    """

    implements(ILogoConfig)

    def collect_scales(self, base_img):
        for scale in SCALES['LOGOS']:
            self.add_scale(scale, convert(base_img, scale))


class IconConfigOverride(AbstractConfigOverride):
    """Icon config (TTW) overrides.
    """

    implements(IIconConfig)

    def collect_scales(self, base_img):
        for scale in SCALES['ICONS']:
            self.add_scale(scale, convert(base_img, scale))
