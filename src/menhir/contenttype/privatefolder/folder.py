# -*- coding: utf-8 -*-

import dolmen.content
from zope.interface import Interface, implements
from dolmen.app.content import icon
from menhir.contenttype.folder import Folder, MCFMessageFactory as _


class IPrivateFolder(Interface):
    """Marker interface for private folders.
    """


class PrivateFolder(Folder):
    icon('folder.png')
    implements(IPrivateFolder)
    dolmen.content.name(_(u"Private folder"))
