import json
from Products.Five.browser import BrowserView
from plone import api


class WebmanifestView(BrowserView):

    def __call__(self):
        portal_url = api.portal.get().absolute_url()
        response = self.request.response
        response.setHeader('Content-Type', 'application/json')

        return json.dumps({
            'name': 'logo',
            'short_name': 'logo',
            'icons': [
                {
                    'src': '{}/@@logo/icon/ANDROID_192X192'.format(portal_url),
                    'sizes': '192x192',
                    'type': 'image/png'
                },
                {
                    'src': '{}/@@logo/icon/ANDROID_512X512'.format(portal_url),
                    'sizes': '512x512',
                    'type': 'image/png'
                }
            ],
            'theme_color': '#ffffff',
            'background_color': '#ffffff',
            'display': 'standalone'
            })

