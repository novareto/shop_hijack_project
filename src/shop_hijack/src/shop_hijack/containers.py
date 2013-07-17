# -*- coding: utf-8 -*-

from .components import Container
from .models import Shop, Incident, Employee
from .interfaces import IShops, IIncidents, IEmployees
from zope.interface import implementer


@implementer(IShops)
class ShopsRoot(Container):
    pass


@implementer(IIncidents)
class IncidentsRoot(Container):
    pass


@implementer(IEmployees)
class EmployeesRoot(Container):
    pass
