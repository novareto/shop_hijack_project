# -*- coding: utf-8 -*-

from dolmen.breadcrumbs import BreadcrumbsRenderer
from uvc.tb_layout.managers import AboveContent
from uvclight import Viewlet, viewletmanager, require


class Breadcrumbs(BreadcrumbsRenderer, Viewlet):
    require('zope.Public')
    viewletmanager(AboveContent)
    
    def __init__(self, *args, **kws):
        Viewlet.__init__(self, *args, **kws)
