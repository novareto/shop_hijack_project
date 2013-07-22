# -*- coding: utf-8 -*-

from cromlech.browser import request
from cromlech.browser.exceptions import HTTPFound
from dolmen.content import schema
from dolmen.forms.base import DISPLAY, action, FAILURE, SUCCESS
from dolmen.forms.base.utils import Fields, apply_data_event
from dolmen.location import get_absolute_url
from dolmen.menu import menuentry
from dolmen.message import send as website_message
from dolmen.view import name, title
from grokcore.component import baseclass
from grokcore.security import require
from uvc.tb_layout.menus import DocumentActionsMenu
from uvclight import Form, context
from zope.interface import implements

from ..models import Shop, Comment, Incident, Employee
from ..interfaces import IContent, IContainer
from ..interfaces import IShops, IComments, IIncidents, IEmployees


@menuentry(DocumentActionsMenu)
class Edit(Form):
    context(IContent)
    name('edit')
    title(u"Édition")
    require('zope.Public')

    ignoreContent = False

    @property
    def fields(self):
        return Fields(*schema.bind().get(self.context))

    @action(u'Update')
    def apply_changes(self):
        data, errors = self.extractData()
        if errors:
            self.errors = errors
            return FAILURE

        website_message(u"Edition successful.")
        apply_data_event(self.fields, self.getContentData(), data)
        raise HTTPFound(get_absolute_url(self.context, self.request))
        return SUCCESS

    @action(u'Cancel')
    def cancel(self):
        website_message(u"Edition cancelled.")
        url = get_absolute_url(self.context, self.request)
        raise HTTPFound(url)


class Add(Form):
    baseclass()
    context(IContainer)
    name('create')
    title(u"Create a new entry")
    require('zope.Public')

    ignoreContent = True

    @property
    def model(self):
        return self.context.model

    @property
    def fields(self):
        return Fields(*schema.bind().get(self.model))

    @action(u'Add')
    def apply_changes(self):
        data, errors = self.extractData()
        if errors:
            self.errors = errors
            return FAILURE

        obj = self.model(**data)
        self.context.add(obj)

        website_message(u'Creation successful.')
        url = get_absolute_url(self.context, self.request)
        raise HTTPFound(url)

    @action(u'Cancel')
    def cancel(self):
        website_message(u"Creation cancelled.")
        url = get_absolute_url(self.context, self.request)
        raise HTTPFound(url)


@menuentry(DocumentActionsMenu)
class AddShop(Add):
    context(IShops)
    model = Shop


@menuentry(DocumentActionsMenu)
class AddEmployee(Add):
    context(IEmployees)
    model = Employee


@menuentry(DocumentActionsMenu)
class AddIncident(Add):
    context(IIncidents)
    model = Incident


@menuentry(DocumentActionsMenu)
class AddComment(Add):
    context(IComments)
    model = Comment


@menuentry(DocumentActionsMenu)
class Delete(Form):
    context(IContent)
    name('delete')
    title(u"Deletion")
    require('zope.Public')

    label = u"Are you sure you want to delete"

    @action(u'Delete')
    def apply_changes(self):
        container = self.context.__parent__
        container.delete(self.context)

        website_message(u'Object successfully deleted.')
        url = get_absolute_url(container, self.request)
        raise HTTPFound(url)

    @action(u'Cancel')
    def cancel(self):
        website_message(u"Deletion cancelled.")
        url = get_absolute_url(self.context, self.request)
        raise HTTPFound(url)
