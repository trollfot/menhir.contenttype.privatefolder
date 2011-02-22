# -*- coding: utf-8 -*-

import dolmen.content
from dolmen.app.content import icon
from menhir.contenttype.folder import Folder, IFolder, MCFMessageFactory as _


class IPrivateFolder(IFolder):
    """Schema interface for private folders.
    """


class PrivateFolder(Folder):
    icon('folder.png')
    dolmen.content.schema(IPrivateFolder)
    dolmen.content.name(_(u"Private folder"))
