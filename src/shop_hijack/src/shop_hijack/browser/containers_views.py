# -*- coding: utf-8 -*-

from . import get_template
from ..app import Root
from ..containers import Incidents, Shops, Employees
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
    context(Incidents)
    template = get_template('incidents.pt')

    def url(self, item):
        return get_absolute_url(item, self.request)


class EmployeesList(Page):
    """
    """
    name('index')
    context(Employees)
    template = get_template('employees.pt')

    def url(self, item):
        return get_absolute_url(item, self.request)


class ShopsList(Page):
    """
    """
    name('index')
    context(Shops)
    template = get_template('shops.pt')

    def url(self, item):
        return get_absolute_url(item, self.request)
