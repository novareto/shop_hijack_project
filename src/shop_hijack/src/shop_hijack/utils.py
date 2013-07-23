# -*- coding: utf-8 -*-

from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from zope.component.hooks import setSite
from zope.component import queryMultiAdapter
from .REST import methods, IRESTRequest


FALLBACK = "GET"


def restful_query_view(request, obj, name=""):
    method = request.method
    target = methods.get(method)
    result = queryMultiAdapter((obj, request), target, name=name)
    if result is None and method != FALLBACK:
        result = queryMultiAdapter((obj, request), target, name=name)
    return result


def view_querier(request, obj, name=""):
    if IRESTRequest.providedBy(request):
        return restful_query_view(request, obj, name)
    return query_view(request, obj, name)


view_lookup = ViewLookup(view_locator(view_querier))


class Site(object):

    def __init__(self, root):
        self.root = root

    def __enter__(self):
        setSite(self.root)
        return self.root

    def __exit__(self, exc_type, exc_value, traceback):
        setSite()

