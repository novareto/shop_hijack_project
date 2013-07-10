# -*- coding: utf-8 -*-

from . import DB_KEY
from .models import Shop, Employee, Incident
from .interfaces import IShop, IEmployee, IIncident
from cromlech.sqlalchemy import get_session
from zope.location import Location, LocationProxy, locate


class SQLContainer(Location):

    model = None
    key_converter = None

    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, id):
        if self.key_converter is not None:
            key = self.key_converter(id)
        else:
            key = id

        session = get_session(DB_KEY)
        model = session.query(self.model).get(key)
        
        if model is None:
            raise KeyError(key)
        proxy = LocationProxy(model)
        locate(proxy, self, str(id))
        return proxy

    def query_filters(self, query):
        return query
        
    def __iter__(self):
        session = get_session(DB_KEY)
        models = self.query_filters(session.query(self.model))
        return iter(models)

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


class Shops(SQLContainer):
    """A root container, to start browsing from shops
    """
    model = Shop
    key_converter = int


class Employees(SQLContainer):
    """A root container, to start browsing from employees
    """
    model = Employee
    key_converter = int


class Incidents(SQLContainer):
    """A root container, to start browsing from incidents
    """
    model = Incident
    key_converter = int

    def query_filters(self, query):
        return query.order_by(model.date.desc())
