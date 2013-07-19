# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.ztk.widgets.collection import CollectionSchemaField
from dolmen.forms.ztk.widgets.collection import MultiChoiceWidgetExtractor, MultiChoiceFieldWidget
from zope.schema import interfaces as schema_interfaces
from dolmen.forms.ztk.widgets.choice import ChoiceSchemaField
from zope.interface import Interface
from dolmen.forms.ztk.fields import registerSchemaField
from dolmen.forms.base.widgets import WidgetExtractor


class MappingSchemaField(CollectionSchemaField):
    """A set field
    """
    collectionType = dict


def register():
    registerSchemaField(MappingSchemaField, schema_interfaces.IDict)


class DictFieldWidget(MultiChoiceFieldWidget):
    grok.adapts(MappingSchemaField, ChoiceSchemaField, Interface, Interface)

    def prepareContentValue(self, value):
        form_value = {}
        if value is NO_VALUE:
            return {self.identifier: form_value}
        choices = self.choices()
        for entry in value:
            try:
                term = choices.getTermByToken(entry)
                form_value[term.token] = term.value
            except LookupError:
                pass

        return {self.identifier: form_value}


class DictWidgetExtractor(WidgetExtractor):
    grok.adapts(MappingSchemaField, ChoiceSchemaField, Interface, Interface)

    def __init__(self, field, value_field, form, request):
        super(DictWidgetExtractor, self).__init__(field, form, request)
        self.source = value_field

    def extract(self):
        value, errors = super(DictWidgetExtractor, self).extract()
        if errors is None:
            is_present = self.request.form.get(
                self.identifier + '.present', NO_VALUE)
            if is_present is NO_VALUE:
                # Not in the request
                return (NO_VALUE, None)
            if value is NO_VALUE:
                # Nothing selected
                return (self.component.collectionType(), None)
            choices = self.source.getChoices(self.form.context)
            try:
                if not isinstance(value, list):
                    value = [value]
                value = self.component.collectionType(
                    [(t, choices.getTermByToken(t).value) for t in value])
            except LookupError:
                return (None, _(u'The selected value is not available.'))
        return (value, errors)

    def extractRaw(self):
        entries = {}
        sub_identifier = self.identifier + '.'
        for key, value in self.request.form.iteritems():
            if key.startswith(sub_identifier) or key == self.identifier:
                entries[key] = value
        return entries
