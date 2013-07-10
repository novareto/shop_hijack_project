# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Text
from zope.interface import implementer

from . import Base
from .interfaces import IComment, IIncident, IEmployee, IShop


@implementer(IComment)
class Comment(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    __tablename__ = 'comments'

    id = Column('id', Integer, primary_key=True)
    incident_id = Column('incident_id', Integer, ForeignKey('incidents.id'))
    date = Column('date', DateTime)
    text = Column('text', Text)


@implementer(IIncident)
class Incident(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    __tablename__ = 'incidents'

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    date = Column('date', DateTime)
    type = Column('type', String(128))

    comments = relationship(
        "Comment", backref="incident",
        collection_class=set, cascade="all, delete-orphan")


@implementer(IEmployee)
class Employee(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    __tablename__ = 'employees'

    id = Column('id', Integer, primary_key=True)
    shop_id = Column('shop_id', Integer, ForeignKey('shops.id'))
    fullname = Column('fullname', String(255))
    position = Column('position', String(255))


@implementer(IShop)
class Shop(Base):
    """TODO: we want a docstring. Just do it _/.
    """
    __tablename__ = 'shops'

    id = Column('id', Integer, primary_key=True)
    address = Column('address', Text)
    
    incidents = relationship(
        "Incident", backref="shop", collection_class=set,
        cascade="all, delete-orphan")

    employees = relationship(
        "Employee", backref="shop",
        collection_class=set, cascade="all, delete-orphan")
