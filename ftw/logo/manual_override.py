from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema

from ftw.logo import _

class IManualOverrides(model.Schema):

    base_logo = NamedBlobImage(
        title = _(u"SVG base logo"),
        required=False,
    )

    standard_logo = NamedBlobImage(
        title = _(u"Standard (desktop) logo (PNG)"),
        required=False,
    )

    mobile_logo = NamedBlobImage(
        title = _(u"Mobile logo (PNG)"),
        required=False,
    )

    base_icon = NamedBlobImage(
        title = _(u"SVG base icon"),
        required=False,
    )

    apple_touch_icon = NamedBlobImage(
        title = _(u"Apple touch icon"),
        required=False,
    )

    favicon_32 = NamedBlobImage(
        title = _(u"Favicon 32x32"),
        required=False,
    )

    favicon_16 = NamedBlobImage(
        title = _(u"Favicon 16x16"),
        required=False,
    )

    mstile_150 = NamedBlobImage(
        title = _(u"Mstile icon 150x150"),
        required=False,
    )

    android_192 = NamedBlobImage(
        title = _(u"Android icon 192x192"),
        required=False,
    )

    android_512 = NamedBlobImage(
        title = _(u"Android icon 512x512"),
        required=False,
    )

    favicon = NamedBlobImage(
        title = _(u"Favicon"),
        required=False,
    )
