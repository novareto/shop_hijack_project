# -*- coding: utf-8 -*-

from uvclight import Form, context
from uvc.layout.slots.menus import DocumentActionsMenu
from cromlech.browser import request
from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base import DISPLAY, action, FAILURE, SUCCESS
from dolmen.forms.base.utils import Fields, apply_data_event
from dolmen.location import get_absolute_url
from dolmen.message import send as website_message
from dolmen.view import name, title
from dolmen.content import schema
from grokcore.security import require
from grokcore.component import baseclass
from zope.interface import implements
from ..interfaces import IContent, IContainer
from dolmen.menu import menuentry


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


@menuentry(DocumentActionsMenu)
class Add(Form):
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
        return Fields(*schema.bind().get(self.context.model))
        
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
