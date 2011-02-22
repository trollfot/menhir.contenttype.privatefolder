#!/usr/bin/python
# -*- coding: utf-8 -*-

import grokcore.view as grok

from dolmen import menu
from dolmen.app.container import listing
from dolmen.app.layout import Page, Form
from dolmen.app.viewselector import SelectableViewsMenu
from menhir.contenttype.privatefolder import IPrivateFolder
from zope.component import getMultiAdapter
from menhir.contenttype.privatefolder import MCFMessageFactory as _
from zeam.form.table import TableActions
from zeam.form.table.form import TableFormCanvas
from zeam.form.ztk.fields import SchemaField
from zeam.form.ztk.actions import EditAction
from zeam.form.ztk.widgets.choice import ChoiceSchemaField
from zope.schema import Choice, TextLine
from zope.securitypolicy.settings import Allow, Deny, Unset
from zeam.form.base import Fields, Actions, Action, SUCCESS, DISPLAY
from zeam.form.base.markers import NO_VALUE, SUCCESS, FAILURE
from zeam.form.base.interfaces import IField, IDataManager
from zeam.form.base.form import cloneFormData
from zope.security.interfaces import IPermission
from zope.component import getUtilitiesFor
from zope.securitypolicy.interfaces import IRole
from zeam.form.base.form import FormData
import megrok.pagetemplate as pt
from zeam.form.base.widgets import Widgets, getWidgetExtractor
from zeam.form.table.select import SelectField
from zeam.form.base.datamanager import ObjectDataManager
from zope.securitypolicy.interfaces import IRolePermissionManager
from zope.interface import implements


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

        context = form.getContent()
        self.applyData(content, data)
        form.status = _(u"Modification saved.")
        return SUCCESS


class PermissionsFields(object):

    def __set__(self, inst, value):
        pass

    def __get__(self, inst, klass):
        if inst is None:
            return None

        value = inst.__dict__.get('_permissions', None)
        if value is None:
            rpm = IRolePermissionManager(inst.getContentData().getContent())
            value = inst.__dict__['_permissions'] = Fields()
            for name, permission in getUtilitiesFor(IRole):
                value.append(ChoiceSchemaField(Choice(
                    __name__=permission.id,
                    title=permission.title,
                    values=[Allow.getName(),
                            Deny.getName(),
                            Unset.getName()])))
        return value


class PermissionWrapper(object):
    implements(IDataManager)

    def __init__(self, permission, manager):
        self.permission = permission
        self.manager = manager
        self.title = permission.title

    def getContent(self):
        return self

    def get(self, name):
        if hasattr(self, name):
            return self.__getattribute__(name)
        return self.manager.getSetting(
            self.permission.id, name, default=Unset).getName()

    def set(self, id, value):
        if value is Unset.getName():
            self.manager.unsetPermissionFromRole(self.permission.id, id)
        elif value is Deny.getName():
            self.manager.denyPermissionToRole(self.permission.id, id)
        elif value is Allow.getName():
            self.manager.grantPermissionToRole(self.permission.id, id)


class ControlByRole(TableFormCanvas, Form):
    grok.context(IPrivateFolder)
    actions = Actions()
    fields = Fields()
    tableFields = PermissionsFields()
    tableActions = TableActions(Apply())

    items = None
    ignoreContent = False

    def updateLines(self, mark_selected=False):
        self.lines = []
        self.lineWidgets = []
        manager = IRolePermissionManager(self.getContent())

        for position, item in enumerate(self.getItems()):
            prefix = '%s.line-%d' % (self.prefix, position)
            form = cloneFormData(
                self, content=PermissionWrapper(item, manager), prefix=prefix)
            form.selected = False

            title = SchemaField(TextLine(
                __name__="title",
                title=u"title",
                default=unicode(item.title)))
            title.mode = DISPLAY
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
            lineWidget.extend(title)
            self.lines.append(form)
            self.lineWidgets.append(lineWidget)

    def getItems(self):
        if not self.items:
            self.items = []
            for name, permission in getUtilitiesFor(IPermission):
                if not name.startswith('zope.'):
                    self.items.append(permission)
        return self.items


class TableForm(pt.PageTemplate):
    grok.view(ControlByRole)
