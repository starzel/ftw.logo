from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class LogoViewlet(ViewletBase):

    index = ViewPageTemplateFile('logo_viewlet.pt')

    def update(self):
        super(LogoViewlet, self).update()
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.navigation_root_url = self.portal_state.navigation_root_url()
