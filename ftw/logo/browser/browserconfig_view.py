from Products.Five.browser import BrowserView
from plone import api


class BrowserconfigView(BrowserView):

    def __call__(self):
        portal_url = api.portal.get().absolute_url()
        response = self.request.response
        response.setHeader('Content-Type', 'text/xml')

        return (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<browserconfig>'
            '<msapplication>'
            '<tile>'
            '<square150x150logo src="{}/@@logo/icon/MSTILE_150X150"/>'
            '<TileColor>#da532c</TileColor>'
            '</tile>'
            '</msapplication>'
            '</browserconfig>').format(portal_url)
