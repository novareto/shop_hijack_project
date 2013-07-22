# -*- coding: utf-8 -*-

from dolmen.viewlet import Viewlet
from dolmen.breadcrumbs import BreadcrumbsRenderer
from cromlech.browser import slot
from grokcore.security import require
from uvc.tb_layout.managers import AboveContent


class Breadcrumbs(BreadcrumbsRenderer, Viewlet):
    require('zope.Public')
    slot(AboveContent)
    
    def __init__(self, *args, **kws):
        Viewlet.__init__(self, *args, **kws)
