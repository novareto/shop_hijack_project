# -*- coding: utf-8 -*-

from . import DB_KEY
from .interfaces import IShop, IEmployee, IIncident, IContainer

from cromlech.sqlalchemy import get_session
from sqlalchemy.orm.collections import MappedCollection, collection
from sqlalchemy.orm.util import identity_key
from zope.interface import implementer
from zope.location import ILocation, Location, LocationProxy, locate


def default_keyfunc(node):
    primary_keys = node.__table__.primary_key.columns.keys()
    if len(primary_keys) == 1:
        return getattr(node, primary_keys[0])
    else:
        raise RuntimeError(
            "don't know how to do keying with composite primary keys")


@implementer(IContainer, ILocation)
class Container(object):

    def __init__(self, parent, name, model, key_converter=int):
        self.__parent__ = parent
        self.__name__ = name
        self.model = model
        self.key_converter = key_converter

    def __getitem__(self, id):
        if self.key_converter is not None:
            try:
                key = self.key_converter(id)
            except ValueError as e:
                raise KeyError(id)
        else:
            key = id

        session = get_session(DB_KEY)
        model = session.query(self.model).get(key)

        if model is None:
            raise KeyError(key)

        locate(model, self, unicode(id))
        return model

    def __iter__(self):
        session = get_session(DB_KEY)
        models = session.query(self.model)
        return iter([LocationProxy(model, self, unicode(model.id))
                     for model in models])

    def values(self):
        return iter(self)

    def add(self, item):
        try:
            session = get_session(DB_KEY)
            session.add(item)
        except Exception, e:
            # This might be a bit too generic
            return e

    def delete(self, item):
        session = get_session(DB_KEY)
        session.delete(item)


@implementer(IContainer, ILocation)
class Collection(MappedCollection):

    __parent__ = None
    __name__ = None

    def __init__(self, *args, **kw):
        MappedCollection.__init__(self, keyfunc=default_keyfunc)

    @collection.linker
    def on_link(self, adapter):
        if adapter is not None:
            self.__parent__ = adapter.owner_state.obj()
            self.__name__ = unicode(adapter.attr.key)
        else:
            # unlinking collection from parent
            self.__parent__ = None
            self.__name__ = None

    def __setitem__(self, key, item):
        key = unicode(key)
        self._receive(item, key)
        MappedCollection.__setitem__(self, key, item)

    def __delitem__(self, key):
        key = unicode(key)
        self._release(self[key])
        MappedCollection.__delitem__(self, key)

    def _receive(self, item, key):
        item.__name__ = key
        item.__parent__ = self

    def _release(self, item):
        del item.__name__
        del item.__parent__

    @collection.internally_instrumented
    @collection.appender
    def set(self, value, _sa_initiator=None):
        key = self.keyfunc(value)
        if key is None:
            session = get_session(DB_KEY)
            session.flush()
            key = self.keyfunc(value)
        self.__setitem__(key, value, _sa_initiator)

    @collection.iterator
    def values(self):
        for key, value in self.items():
            self._receive(value, key)
            yield value

    @collection.converter
    def convert(self, other):
        if isinstance(other, (list, set, tuple)):
            return other
        if isinstance(other, dict):
             return other.values()
        raise ValueError
