from plone import api
from plone.dexterity.browser import add, edit
from plone.dexterity.content import Item
from plone.formwidget.namedfile import NamedImageFieldWidget
from plone.namedfile.field import NamedBlobImage
from plone.protect.auto import safeWrite
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import transaction
from zope import schema
from zope.component import adapter
from zope.interface import Invalid
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from ftw.logo import _
from ftw.logo.collector import collect_icons
from ftw.logo.collector import collect_logos
from ftw.logo.logoconfig import IconConfigOverride
from ftw.logo.logoconfig import LogoConfigOverride

OVERRIDES_FIXED_ID = 'ftw-logo-overrides'

def svg_file_only(value):
    if value.contentType != 'image/svg+xml':
        raise Invalid(
            u"This image must be a SVG file " +
            u"({} supplied)".format(value.contentType)
        )
    return True

def png_file_only(value):
    if value.contentType != 'image/png':
        raise Invalid(
            u"This image must be a PNG file " +
            u"({} supplied)".format(value.contentType)
        )
    return True

class IManualOverrides(model.Schema):

    # Note: The field names are carefully constructed as one of:
    #   logo_<logo scale name>, or
    #   icon_<icon scale name>
    # The form (manual_override.pt) depends on this to find the ZCML
    # default image

    logo_BASE = NamedBlobImage(
        title = _(u"SVG base logo"),
        description = _(u"Overriding the base logo will generate an override "
                        u"for BOTH logos below if not already set."),
        required=False,
        constraint=svg_file_only,
    )

    logo_LOGO = NamedBlobImage(
        title = _(u"Standard (desktop) logo (PNG)"),
        required=False,
        constraint=png_file_only,
    )

    logo_MOBILE_LOGO = NamedBlobImage(
        title = _(u"Mobile logo (PNG)"),
        required=False,
        constraint=png_file_only,
    )

    icon_BASE = NamedBlobImage(
        title = _(u"SVG base icon"),
        description = _(u"Overriding the base icon will generate an "
                        u"override for ALL icons below if not already set."),
        required=False,
        constraint=svg_file_only,
    )

    icon_APPLE_TOUCH_ICON = NamedBlobImage(
        title = _(u"Apple touch icon"),
        required=False,
        constraint=png_file_only,
    )

    icon_FAVICON_32X32 = NamedBlobImage(
        title = _(u"Favicon 32x32"),
        required=False,
        constraint=png_file_only,
    )

    icon_FAVICON_16X16 = NamedBlobImage(
        title = _(u"Favicon 16x16"),
        required=False,
        constraint=png_file_only,
    )

    icon_MSTILE_150X150 = NamedBlobImage(
        title = _(u"Mstile icon 150x150"),
        required=False,
        constraint=png_file_only,
    )

    icon_ANDROID_192X192 = NamedBlobImage(
        title = _(u"Android icon 192x192"),
        required=False,
        constraint=png_file_only,
    )

    icon_ANDROID_512X512 = NamedBlobImage(
        title = _(u"Android icon 512x512"),
        required=False,
        constraint=png_file_only,
    )

    icon_FAVICON = NamedBlobImage(
        title = _(u"Favicon"),
        required=False,
        constraint=png_file_only,
    )


class ManualOverrides(Item):
    """A custom content class"""

    def __init__(self, id=None):
        super(ManualOverrides, self).__init__(id)
        logo_overrides = None
        icon_overrides = None


@adapter(IManualOverrides, IObjectModifiedEvent)
def overrides_changed(override_object, event):
    if override_object.logo_BASE:
        override_object.logo_overrides = LogoConfigOverride(override_object.logo_BASE)
        collect_logos(override_object.logo_overrides)
    if override_object.icon_BASE:
        override_object.icon_overrides = IconConfigOverride(override_object.icon_BASE)
        collect_icons(override_object.icon_overrides)

class CreateOverridesIfReqdForm(BrowserView):
    """
    Create IManualOverrides if it does not exist and redirect to it's edit form
    """
    def __call__(self):
        navroot = self.context
        overridesItem = navroot.get(OVERRIDES_FIXED_ID)
        if overridesItem is None:
            safeWrite(navroot, self.request)

            overridesItem = api.content.create(
                type='ftw.logo.ManualOverrides',
                title='Logo and Icon Overrides',
                description='Manual overrides for the site logo(s) and icons',
                id=OVERRIDES_FIXED_ID,
                safe_id=True,
                container=navroot
            )
            transaction.get().commit()

        self.request.response.redirect('{}/@@edit'.format(
            overridesItem.absolute_url_path()
        ))
        return ""


class EditManualOverrideForm(edit.DefaultEditForm):
    label = _(u"Edit Manual Logo and Icon Overrides")
    description = _(u"Site logos and icons set in ZCML are shown in " +
                    u"the left column. Overrides from this form are " +
                    u"shown in the right column")

    template = ViewPageTemplateFile('manual_override.pt')

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        super(EditManualOverrideForm, self).update()
