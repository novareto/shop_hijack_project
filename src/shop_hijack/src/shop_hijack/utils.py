# -*- coding: utf-8 -*-

from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from zope.component.hooks import setSite


view_lookup = ViewLookup(view_locator(query_view))


class Site(object):

    def __init__(self, root):
        self.root = root
    
    def __enter__(self):
        setSite(self.root)
        return self.root
        
    def __exit__(self, exc_type, exc_value, traceback):
        setSite()

