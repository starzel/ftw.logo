from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogo
from ftw.logo.interfaces import ILogoConfig
from plone.app.layout.globals.interfaces import IViewView
from Products.Five.browser import BrowserView
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from ZPublisher.Iterators import filestream_iterator
import mimetypes


CONFIGS = {
    'logo': ILogoConfig,
    'icon': IIconConfig,
}
SCALES = ('base',)


@implementer(IPublishTraverse, IViewView)
class LogoView(BrowserView):

    def __init__(self, context, request):
        super(LogoView, self).__init__(context, request)
        self.scale = None
        self.config = None

    def publishTraverse(self, request, name):
        if name in CONFIGS:
            self.config = CONFIGS[name]
            return self
        elif self.config and name in SCALES:
            self.scale = name
            return self
        elif self.config and self.scale:
            return self
        else:
            raise NotFound()

    def __call__(self):
        if not self.config or not self.scale:
            raise BadRequest()
        path = getattr(getMultiAdapter((self.context, self.request),
                                       ILogo).get_config(self.config), self.scale)
        response = self.request.response
        contenttype = mimetypes.guess_type(
            path)[0] or 'application/octet-stream'
        file_iterator = filestream_iterator(path)
        response.setHeader('Content-Type', contenttype)
        response.setHeader('Content-Length', file_iterator.__len__())
        return file_iterator
