from plone import api
from plone.dexterity.browser import add, edit
from plone.formwidget.namedfile import NamedImageFieldWidget
from plone.namedfile.field import NamedBlobImage
from plone.protect.auto import safeWrite
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import transaction
from zope import schema

from ftw.logo import _

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
    )

    logo_LOGO = NamedBlobImage(
        title = _(u"Standard (desktop) logo (PNG)"),
        required=False,
    )

    logo_MOBILE_LOGO = NamedBlobImage(
        title = _(u"Mobile logo (PNG)"),
        required=False,
    )

    icon_BASE = NamedBlobImage(
        title = _(u"SVG base icon"),
        description = _(u"Overriding the base icon will generate an "
                        u"override for ALL icons below if not already set."),
        required=False,
    )

    icon_APPLE_TOUCH_ICON = NamedBlobImage(
        title = _(u"Apple touch icon"),
        required=False,
    )

    icon_FAVICON_32X32 = NamedBlobImage(
        title = _(u"Favicon 32x32"),
        required=False,
    )

    icon_FAVICON_16X16 = NamedBlobImage(
        title = _(u"Favicon 16x16"),
        required=False,
    )

    icon_MSTILE_150X150 = NamedBlobImage(
        title = _(u"Mstile icon 150x150"),
        required=False,
    )

    icon_ANDROID_192X192 = NamedBlobImage(
        title = _(u"Android icon 192x192"),
        required=False,
    )

    icon_ANDROID_512X512 = NamedBlobImage(
        title = _(u"Android icon 512x512"),
        required=False,
    )

    icon_FAVICON = NamedBlobImage(
        title = _(u"Favicon"),
        required=False,
    )


class CreateOverridesIfReqdForm(BrowserView):
    """
    Create IManualOverrides if it does not exist and redirect to it's edit form
    """
    def __call__(self):
        navroot = self.context
        override_item_id = 'ftw-logo-overrides'
        overridesItem = navroot.get(override_item_id)
        if overridesItem is None:
            safeWrite(navroot, self.request)

            overridesItem = api.content.create(
                type='ftw.logo.ManualOverrides',
                title='Logo and Icon Content',
                id=override_item_id,
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
