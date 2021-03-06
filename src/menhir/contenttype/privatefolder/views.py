#!/usr/bin/python
# -*- coding: utf-8 -*-

import grokcore.view as grok
import megrok.pagetemplate as pt

from dolmen import menu
from dolmen.app.layout import ContextualMenu, Form
from menhir.contenttype.privatefolder import IPrivateFolder
from menhir.contenttype.privatefolder import MCFMessageFactory as _
from zeam.form.base import Fields, Actions, Action, DISPLAY
from zeam.form.base.form import cloneFormData
from zeam.form.base.interfaces import IDataManager
from zeam.form.base.markers import NO_VALUE, SUCCESS, FAILURE
from zeam.form.base.widgets import Widgets, getWidgetExtractor
from zeam.form.table import TableActions
from zeam.form.table.form import TableFormCanvas
from zeam.form.table.select import SelectField
from zeam.form.ztk.fields import SchemaField
from zeam.form.ztk.widgets.choice import ChoiceSchemaField
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.schema import Choice, TextLine
from zope.security.interfaces import IPermission
from zope.securitypolicy.interfaces import IRole, IRolePermissionManager
from zope.securitypolicy.settings import Allow, Deny, Unset


def sort_items(itemA, itemB):
    return cmp(itemA.id, itemB.id)


def filter_items(items, filters):
    for name, value in items:
        iterate = True
        for filter in filters:
            if not filter(value):
                iterate = False
                break
        if iterate is True:
            yield name, value


def iter_permissions(*filters):
    permissions = getUtilitiesFor(IPermission)
    if not filters:
        return permissions
    return filter_items(permissions, filters)


def iter_roles(*filters):
    roles = getUtilitiesFor(IRole)
    if not filters:
        return roles
    return filter_items(roles, filters)


class Apply(Action):
    title = u"Apply"

    def applyData(self, content, data):
        for name, value in data.items():
            if value is not NO_VALUE:
                content.set(name, value)

    def __call__(self, form, content, line):
        data, errors = line.extractData(form.tableFields)
        if errors:
            return FAILURE

        print data
        self.applyData(content, data)
        form.redirect(form.url(form.context, name="controlbyrole"))
        return SUCCESS


class PermissionsFields(object):

    def __init__(self, *filters):
        self.filters = filters

    def __set__(self, inst, value):
        raise NotImplementedError

    def __get__(self, inst, cls):
        if inst is None:
            return None
        value = inst.__dict__.get('_permissions', None)
        if value is None:
            value = inst.__dict__['_permissions'] = Fields()
            for name, permission in iter_roles(*self.filters):
                value.append(ChoiceSchemaField(
                    Choice(__name__=permission.id,
                           title=permission.title,
                           values=[Allow, Deny, Unset]),
                    ))
        return value


class PermissionWrapper(object):
    implements(IDataManager)

    def __init__(self, permission, manager):
        self.permission = permission
        self.manager = manager

    def getContent(self):
        return self

    def get(self, name):
        return self.manager.getSetting(
            self.permission.id, name, default=Unset)

    def set(self, id, value):
        if value is Unset:
            self.manager.unsetPermissionFromRole(self.permission.id, id)
        elif value is Deny:
            self.manager.denyPermissionToRole(self.permission.id, id)
        elif value is Allow:
            self.manager.grantPermissionToRole(self.permission.id, id)
        else:
            raise ValueError(
                'The given value is not a valid permission setting')


def zopeRealm(item):
    return not item.id.startswith('zope.')


def grokRealm(item):
    return not item.id.startswith('grok.')


class ControlByRole(TableFormCanvas, Form):
    grok.baseclass()

    actions = Actions()
    fields = Fields()
    tableFields = PermissionsFields(zopeRealm)
    tableActions = TableActions(Apply())

    items = None
    ignoreContent = False
    ignoreRequest = False

    def updateLines(self, mark_selected=False):
        self.lines = []
        self.lineWidgets = []
        manager = IRolePermissionManager(self.getContent())

        for position, item in enumerate(self.getItems()):
            prefix = '%s.line-%d' % (self.prefix, position)
            form = cloneFormData(
                self, content=PermissionWrapper(item, manager), prefix=prefix)
            form.selected = False

            titleField = SchemaField(TextLine(
                __name__="title",
                title=u"title",                
                default=u""))
    
            titleField.mode = DISPLAY
            titleField.ignoreRequest = True
            titleField.ignoreContent = True
            titleField.readonly = True
            titleField.defaultValue = item.title
            
            lineWidget = Widgets(form=form, request=self.request)

            # Checkbox to select the line
            selectedField = SelectField(identifier=position)

            if mark_selected:
                # Mark selected lines
                selectedExtractor = getWidgetExtractor(
                    selectedField, form, self.request)
                if selectedExtractor is not None:
                    value, error = selectedExtractor.extract()
                    if value:
                        form.selected = True

            lineWidget.extend(selectedField)
            lineWidget.extend(titleField)
            self.lines.append(form)
            self.lineWidgets.append(lineWidget)

    def getItems(self):
        if not self.items:
            self.items = list(
                (perm for name, perm in
                 iter_permissions(zopeRealm, grokRealm)))
            self.items.sort(sort_items)
        return self.items


class TableForm(pt.PageTemplate):
    grok.view(ControlByRole)
