# -*- coding: utf-8 -*-

from . import get_template
from ..app import Root
from .. import containers
from ..interfaces import IShops, IComments, IEmployees, IIncidents
from uvclight import Page, context, name
from dolmen.location import get_absolute_url


class RootIndex(Page):
    """
    """
    name('index')
    context(Root)
    template = get_template('root.pt')


class IncidentsList(Page):
    """
    """
    name('index')
    context(IIncidents)
    template = get_template('incidents.pt')

    def url(self, item):
        return get_absolute_url(item, self.request)


class EmployeesList(Page):
    """
    """
    name('index')
    context(IEmployees)
    template = get_template('employees.pt')

    def url(self, item):
        return get_absolute_url(item, self.request)


class ShopsList(Page):
    """
    """
    name('index')
    context(IShops)
    template = get_template('shops.pt')

    def url(self, item):
        return get_absolute_url(item, self.request)
