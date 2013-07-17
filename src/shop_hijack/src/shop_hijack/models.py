# -*- coding: utf-8 -*-

from dolmen.content import schema
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text
from zope.interface import implementer
from zope.location import Location, LocationProxy, locate, ILocation

from . import Base, components
from .interfaces import IComment, IIncident, IEmployee, IShop
from .interfaces import IComments, IIncidents, IEmployees, IShops

import grokcore.component as grok
from dawnlight import DEFAULT
from cromlech.dawnlight.consume import traverse
from dawnlight.interfaces import IConsumer
from cromlech.browser.interfaces import ITraverser
from cromlech.dawnlight.directives import traversable
from zope.interface import Interface
from zope.component import queryMultiAdapter


_marker = object()


@implementer(IShops)
class Shops(components.Collection):
    pass


@implementer(IEmployees)
class Employees(components.Collection):
    pass


@implementer(IIncidents)
class Incidents(components.Collection):
    pass


@implementer(IComments)
class Comments(components.Collection):
    pass


class Content(Location):
    attrs = frozenset()

@implementer(IConsumer)
class LocationAttributesConsumer(grok.Subscription):
    grok.context(Content)
    grok.order(1200)

    __call__ = traverse

    def _resolve(self, obj, ns, name, request):
        name = name.encode('utf-8') if isinstance(name, unicode) else name
        traversables_attrs = self.context.attrs
        if ns == DEFAULT and name in traversables_attrs:
            attr = getattr(obj, name, _marker)
            if attr is not _marker:
                return attr
        return None


class Comment(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IComment)
    __tablename__ = 'comments'

    attrs = frozenset(('incidents',))

    id = Column('id', Integer, primary_key=True)
    incident_id = Column('incident_id', Integer, ForeignKey('incidents.id'))
    date = Column('date', DateTime)
    text = Column('text', Text)


class Incident(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IIncident)
    __tablename__ = 'incidents'

    attrs = frozenset(('shop', 'comments'))

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    date = Column('date', DateTime)
    type = Column('type', String(128))

    comments = relationship(
        "Comment", backref="incident",
        collection_class=Comments, cascade="all, delete-orphan")


class Employee(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IEmployee)
    __tablename__ = 'employees'

    attrs = frozenset(('shop',))

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    fullname = Column('fullname', String(255))
    position = Column('position', String(255))


class Shop(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IShop)
    __tablename__ = 'shops'

    attrs = frozenset(('incidents', 'employees'))

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    address = Column('address', Text)

    incidents = relationship(
        "Incident", backref="shop",
        collection_class=Incidents, cascade="all, delete-orphan")

    employees = relationship(
        "Employee", backref="shop",
        collection_class=Employees, cascade="all, delete-orphan")
