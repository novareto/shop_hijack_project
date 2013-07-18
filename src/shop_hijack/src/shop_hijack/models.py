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
    pass


class Comment(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IComment)
    traversable('incidents')
    
    __tablename__ = 'comments'

    id = Column('id', Integer, primary_key=True)
    incident_id = Column('incident_id', Integer, ForeignKey('incidents.id'))
    date = Column('date', DateTime)
    text = Column('text', Text)


class Incident(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IIncident)
    traversable('shop', 'comments')

    __tablename__ = 'incidents'

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
    traversable('shop')

    __tablename__ = 'employees'

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    fullname = Column('fullname', String(255))
    position = Column('position', String(255))


class Shop(Base, Content):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IShop)
    traversable('incidents', 'employees')

    __tablename__ = 'shops'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    address = Column('address', Text)

    incidents = relationship(
        "Incident", backref="shop",
        collection_class=Incidents, cascade="all, delete-orphan")

    employees = relationship(
        "Employee", backref="shop",
        collection_class=Employees, cascade="all, delete-orphan")
