# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from zope.schema import TextLine, Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


positions = SimpleVocabulary((
    SimpleTerm(value="Manager", title=u"Manager"),
    SimpleTerm(value="Employee", title=u"Employee"),
    ))


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
        vocabulary=('Yes', 'No'),
    )


class IEmployee(IContent):

    fullname = TextLine(
        title=u'Full name'
    )

    position = Choice(
        title=u"Position in the company",
        vocabulary=positions,
    )


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


class IContainer(Interface):

    model = Attribute("The model class")

    def add(item):
        """
        """

    def delete(item):
        """
        """
