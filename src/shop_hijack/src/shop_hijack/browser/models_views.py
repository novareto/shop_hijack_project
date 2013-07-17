# -*- coding: utf-8 -*-

from . import get_template
from ..interfaces import IIncident, IEmployee, IShop
from ..app import ROOT
from uvclight import Page, context, name
from dolmen.location import get_absolute_url


class IncidentView(Page):
    """
    """
    name('index')
    context(IIncident)
    template = get_template('incident.pt')


class EmployeeView(Page):
    """
    """
    name('index')
    context(IEmployee)
    template = get_template('employee.pt')

    def update(self):
        base_url = get_absolute_url(ROOT.shops, self.request)
        self.shop_url = "%s/%s" % (base_url, self.context.shop_id)


class ShopView(Page):
    """
    """
    name('index')
    context(IShop)
    template = get_template('shop.pt')
