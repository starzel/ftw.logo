from ftw.logo.converter import convert
from ftw.logo.converter import SCALES
from ftw.logo.image import Image
from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogoConfig
from hashlib import sha256
from textwrap import wrap
from zope.configuration.exceptions import ConfigurationError
from zope.interface import implements


def get_cachekey_from_blob(*args):
    cachekey = sha256()
    for blob in args:
        if blob:
            for chunk in wrap(blob, 4096):
                cachekey.update(chunk)
    return cachekey.hexdigest()


class AbstractConfig(object):

    logo = None
    mobile_logo = None
    favicon = None

    required_attr = 'logo'

    def __init__(self, **kwargs):
        if self.required_attr not in kwargs:
            raise ConfigurationError('A logo svg/png is required')

        setattr(self, self.required_attr, Image(filename=kwargs[self.required_attr]))

        if 'mobile' in kwargs:
            self.mobile_logo = Image(filename=kwargs['mobile'])
        if 'favicon' in kwargs:
            self.favicon = Image(filename=kwargs['favicon'])

        self.cachekey = get_cachekey_from_blob(
            getattr(self, self.required_attr).make_blob(),
            self.mobile_logo and self.mobile_logo.make_blob() or None,
            self.favicon and self.favicon.make_blob() or None,)
        self.scales = {}
        self.collect_scales()

    def add_scale(self, name, scale):
        self.scales[name] = scale

    def collect_scales(self):
        raise NotImplemented()  # pragma: no cover

    def get_scale(self, name):
        return self.scales[name]


class LogoConfig(AbstractConfig):
    """Logo config entry.
    """

    implements(ILogoConfig)

    def collect_scales(self):
        for scale in SCALES['LOGOS']:
            if getattr(self, scale.lower(), None):
                self.add_scale(scale, convert(getattr(self, scale.lower()), scale))
            else:
                self.add_scale(scale, None)


class IconConfig(AbstractConfig):
    """Icon config entry.
    """

    required_attr = 'base'

    implements(IIconConfig)

    def collect_scales(self):
        for scale in SCALES['ICONS']:
            if getattr(self, scale.lower(), None):
                self.add_scale(scale, convert(getattr(self, scale.lower()), scale))
            else:
                self.add_scale(scale, convert(getattr(self, self.required_attr), scale))


class AbstractConfigOverride(AbstractConfig):

    def __init__(self, blobImage):
        base_img = Image(blob=blobImage.data)
        self.cachekey = get_cachekey_from_blob(blobImage.data)
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
