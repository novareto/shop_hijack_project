# -*- coding: utf-8 -*-

from . import get_template
from ..interfaces import IIncident, IEmployee, IShop
from uvclight import Page, context, name


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


class ShopView(Page):
    """
    """
    name('index')
    context(IShop)
    template = get_template('shop.pt')
