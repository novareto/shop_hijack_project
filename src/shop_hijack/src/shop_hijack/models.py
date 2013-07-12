# -*- coding: utf-8 -*-

from dolmen.content import schema
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text
from zope.interface import implementer

from . import Base
from .interfaces import IComment, IIncident, IEmployee, IShop


class Comment(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IComment)
    __tablename__ = 'comments'

    id = Column('id', Integer, primary_key=True)
    incident_id = Column('incident_id', Integer, ForeignKey('incidents.id'))
    date = Column('date', DateTime)
    text = Column('text', Text)


class Incident(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IIncident)
    __tablename__ = 'incidents'

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    date = Column('date', DateTime)
    type = Column('type', String(128))

    comments = relationship(
        "Comment", backref="incident",
        collection_class=set, cascade="all, delete-orphan")
    

class Employee(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IEmployee)
    __tablename__ = 'employees'

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    fullname = Column('fullname', String(255))
    position = Column('position', String(255))


class Shop(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    schema(IShop)
    __tablename__ = 'shops'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    address = Column('address', Text)
    
    incidents = relationship(
        "Incident", backref="shop", collection_class=set,
        cascade="all, delete-orphan")

    employees = relationship(
        "Employee", backref="shop",
        collection_class=set, cascade="all, delete-orphan")
