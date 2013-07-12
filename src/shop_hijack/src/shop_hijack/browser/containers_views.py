# -*- coding: utf-8 -*-

from . import get_template
from ..app import Root
from ..containers import Incidents, Shops, Employees
from uvclight import Page, context, name
from cromlech.browser import IURL
from zope.component import getMultiAdapter


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
        return str(getMultiAdapter((item, self.request), IURL, u''))

    
class EmployeesList(Page):
    """
    """
    name('index')
    context(Employees)
    template = get_template('employees.pt')

    def url(self, item):
        return str(getMultiAdapter((item, self.request), IURL, u''))
    

class ShopsList(Page):
    """
    """
    name('index')
    context(Shops)
    template = get_template('shops.pt')

    def url(self, item):
        return str(getMultiAdapter((item, self.request), IURL, u''))
