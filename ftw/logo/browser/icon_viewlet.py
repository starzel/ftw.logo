from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IconViewlet(ViewletBase):

    index = ViewPageTemplateFile('icon_viewlet.pt')
