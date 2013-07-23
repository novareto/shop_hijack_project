# -*- coding: utf-8 -*-

from cromlech.browser import IView
from zope.interface import Interface, Attribute
from zope.schema import TextLine, Choice, Text, Set, Date, Dict
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from .vocabularies import ShopSource, EmployeeSource


positions = SimpleVocabulary((
    SimpleTerm(value="Manager", title=u"Manager"),
    SimpleTerm(value="Employee", title=u"Employee"),
    ))


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


class IContent(Interface):
    pass


class IComment(IContent):
    pass


class IIncident(IContent):

    date = Date(
        title=u"Date of the Hijack",
    )

    weapons = Choice(
        title=u"Weapons",
        values=('Yes', 'No'),
    )


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

    mnr = TextLine(
        title=u"Member Id",
    )

    name = TextLine(
        title=u"Name",
    )

    street = TextLine(
        title=u"Street",
    )

    nr = TextLine(
        title=u"Number"
    )

    plz = TextLine(
        title=u"Number of district"
    )

    place = TextLine(
        title=u"Place"
    )

    employees = Dict(
        title=u"Employees in the company",
        value_type=Choice(source=EmployeeSource(id_only=False)),
        required=False)


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
