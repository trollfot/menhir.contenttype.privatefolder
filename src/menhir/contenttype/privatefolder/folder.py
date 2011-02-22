# -*- coding: utf-8 -*-

import dolmen.content
from dolmen.app.content import icon, IDescriptiveSchema
from menhir.contenttype.folder import MCFMessageFactory as _


class IPrivateFolder(IDescriptiveSchema):
    """Schema interface for private folders.
    """


class PrivateFolder(dolmen.content.OrderedContainer):
    icon('folder.png')
    dolmen.content.schema(IPrivateFolder)
    dolmen.content.name(_(u"Private folder"))
    selected_view = "folderlisting"
