from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LogoViewlet(ViewletBase):

    index = ViewPageTemplateFile('logo_viewlet.pt')
