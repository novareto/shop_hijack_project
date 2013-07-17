# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component.hooks import getSite
from zope.schema.interfaces import IContextSourceBinder


@implementer(IContextSourceBinder)
class ShopSource(object):

    def __init__(self, id_only=True):
        self.id_only = id_only

    def make_term(self, obj):
        if self.id_only:
            value = obj.id
        else:
            value = obj
        return SimpleTerm(value, token=obj.id, title='%s (%s)'
                          % (obj.name, obj.id))

    def __call__(self, context):
        root = getSite()
        shops = root.shops
        terms = [self.make_term(s) for s in shops]
        return SimpleVocabulary(terms)


@implementer(IContextSourceBinder)
class EmployeeSource(object):

    def __init__(self, id_only=True):
        self.id_only = id_only

    def make_term(self, obj):
        if self.id_only:
            value = obj.id
        else:
            value = obj
        return SimpleTerm(value, token=obj.id, title='%s (%s)'
                          % (obj.fullname, obj.id))

    def __call__(self, context):
        root = getSite()
        employees = root.employees
        terms = [self.make_term(s) for s in employees]
        return SimpleVocabulary(terms)
