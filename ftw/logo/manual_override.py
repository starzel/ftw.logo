from plone.dexterity.browser import add, edit
from plone.formwidget.namedfile import NamedImageFieldWidget
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema

from ftw.logo import _

class IManualOverrides(model.Schema):

    logo_BASE = NamedBlobImage(
        title = _(u"SVG base logo"),
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


class EditManualOverrideForm(edit.DefaultEditForm):
    label = _(u"Edit Manual Logo and Icon Overrides")
    description = _(u"Overrides for different sizes of logo and icon")

    template = ViewPageTemplateFile('manual_override.pt')

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        super(EditManualOverrideForm, self).update()

    #~ def render(self):
        #~ import pdb; pdb.set_trace()
        #~ super(EditManualOverrideForm, self).render()


class AddManualOverrideForm(add.DefaultAddForm):
    portal_type = 'ftw.logo.ManualOverrides'

class AddManualOverrideView(add.DefaultAddView):
    form = AddManualOverrideForm
