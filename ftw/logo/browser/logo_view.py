from ftw.logo.converter import SCALES
from ftw.logo.converter import flatten_scales
from ftw.logo.interfaces import IIconConfig
from ftw.logo.interfaces import ILogo
from ftw.logo.interfaces import ILogoConfig
from ftw.logo.StringIOStreamIterator import StringIOStreamIterator
from plone.app.layout.globals.interfaces import IViewView
from Products.Five.browser import BrowserView
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
import mimetypes


CONFIGS = {
    'logo': ILogoConfig,
    'icon': IIconConfig,
}


@implementer(IPublishTraverse, IViewView)
class LogoView(BrowserView):

    def __init__(self, context, request):
        super(LogoView, self).__init__(context, request)
        self.scale = None
        self.config = None

    def publishTraverse(self, request, name):
        if self.config is None and name in CONFIGS:
            self.config = CONFIGS[name]
            return self
        elif self.config and name in flatten_scales(SCALES):
            self.scale = name
            return self
        else:
            raise NotFound()

    def __call__(self):
        if not self.config or not self.scale:
            raise BadRequest()
        config = getMultiAdapter(
            (self.context, self.request), ILogo).get_config(self.config)
        scale = config.get_scale(self.scale)
        response = self.request.response
        iterator = StringIOStreamIterator(scale.make_blob())
        contenttype = mimetypes.types_map.get('.{}'.format(
            scale.extension), 'application/octet-stream')
        response.setHeader('X-Theme-Disabled', 'True')
        response.setHeader(
            'Content-Type', '{}; charset=utf-8'.format(contenttype))
        response.setHeader('Content-Length', iterator.len)
        return iterator
