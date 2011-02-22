#!/usr/bin/python
# -*- coding: utf-8 -*-

import grokcore.view as grok

from dolmen import menu
from dolmen.app.container import listing
from dolmen.app.layout import Page
from dolmen.app.viewselector import SelectableViewsMenu
from menhir.contenttype.privatefolder import IPrivateFolder
from zope.component import getMultiAdapter
from menhir.contenttype.folder import MCFMessageFactory as _
from zeam.form.table import TableForm
from zope.schema import Choice
from zope.securitypolicy.settings import Allow, Deny, Unset
from zeam.form.base import IField, Fields, Actions, Action, SUCCESS, DISPLAY
from zope.security.interfaces import IPermission
from zope.component import getUtilitiesFor


class Apply(Action):
    title = u"Apply"

    def available(self, form):
        return True

    def __call__(self, form, content, data):
        print content, data
        return SUCCESS


class PermissionsFields(object):
    def __init__(self):
        self.form = form
        self.context = form.getContentData().getContent()

    def __set__(self, inst, value):
        pass

    def __get__(self, inst, klass):
        if inst is None:
            return None

        value = inst.__dict__.get('_permissions', None)
        if value is None:
            value = inst.__dict__['_permissions'] = Fields()
            for permission in getUtilitiesFor(IPermission):
                value.append(IField(Choice(
                    title=permission.title,
                    values=[Allow, Deny, Unset]
                    default=Unset)))
        return value


class ControlByRole(TableForm):
    grok.context(IPrivateFolder)
    actions = Actions()
    fields = Fields()
    tableFields = PermissionsFields()
    tableActions = TableActions(Apply())
