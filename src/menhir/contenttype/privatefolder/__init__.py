from zope.i18nmessageid import MessageFactory

MCFMessageFactory = MessageFactory('menhir.contenttype.folder')

from menhir.contenttype.privatefolder.folder import (
    IPrivateFolder, PrivateFolder)
