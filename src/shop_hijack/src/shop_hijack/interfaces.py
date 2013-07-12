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
    pass


class IEmployee(IContent):
    fullname = TextLine(title=u'Full name')
    position = Choice(title=u"Position in the company",
                      vocabulary=positions)


class IShop(IContent):
    pass


class IContainer(Interface):

    model = Attribute("The model class")
    
    def add(item):
        """
        """

    def delete(item):
        """
        """
