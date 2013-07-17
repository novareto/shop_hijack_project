# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from zope.schema import TextLine, Choice, Text, Set
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from .vocabularies import ShopSource, EmployeeSource


positions = SimpleVocabulary((
    SimpleTerm(value="Manager", title=u"Manager"),
    SimpleTerm(value="Employee", title=u"Employee"),
    ))


class IContent(Interface):
    pass


class IComment(IContent):
    pass


class IIncident(IContent):
    pass


class IEmployee(IContent):

    shop_id = Choice(
        title=u"Shop",
        source=ShopSource(),
        required=True)

    fullname = TextLine(
        title=u'Full name',
        required=True)

    position = Choice(
        title=u"Position in the company",
        vocabulary=positions,
        required=True)


class IShop(IContent):

    name = TextLine(
        title=u'Name',
        required=True)

    address = Text(
        title=u'Address',
        required=True)

    employees = Set(
        title=u"Employees in the company",
        value_type=Choice(source=EmployeeSource(id_only=False)),
        required=True)


class IContainer(Interface):
    pass


class IShops(IContainer):
    pass


class IIncidents(IContainer):
    pass


class IComments(IContainer):
    pass


class IEmployees(IContainer):
    pass
