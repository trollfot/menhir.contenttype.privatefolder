# -*- coding: utf-8 -*-

import dolmen.content
from dolmen.app.content import icon, IDescriptiveSchema
from dolmen.app.viewselector import IViewSelector
from menhir.contenttype.folder import MCFMessageFactory as _


class IPrivateFolder(IDescriptiveSchema, IViewSelector):
    """Schema interface for private folders.
    """


class PrivateFolder(dolmen.content.OrderedContainer):
    icon('folder.png')
    dolmen.content.schema(IPrivateFolder)
    dolmen.content.name(_(u"Folder"))
    selected_view = "folderlisting"
