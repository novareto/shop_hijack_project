# -*- coding: utf-8 -*-

from cromlech.browser import IView, ITypedRequest


class IRESTRequest(ITypedRequest):
    pass


class IPOSTView(IView):
    pass


class IPUTView(IView):
    pass


class IDELETEView(IView):
    pass


class IHEADView(IView):
    pass


class IOPTIONSView(IView):
    pass


methods = {
    "DELETE": IDELETEView,
    "GET": IView,
    "HEAD": IHEADView,
    "OPTIONS": IOPTIONSView,
    "POST": IPOSTView,
    "PUT": IPUTView,
    }
