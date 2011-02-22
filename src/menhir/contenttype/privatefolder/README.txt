=========================
menhir.contenttype.folder
=========================

``menhir.contenttype.folder`` provides a folderish content for
`Dolmen` based `Grok` applications. This folderish type has several
ways to display itself, allowing the editor to chose wether it should
display a summary of the content or a structured and pagined rendering.

Schema
======

A `Folder` does not have a particular schema. It uses only the
`IDescriptiveSchema` from ``dolmen.app.content``, exposing only the
`title` and `description` attributes::

    >>> from dolmen.content import schema
    >>> from menhir.contenttype.folder import Folder
    >>> print schema.bind().get(Folder)
    [<InterfaceClass menhir.contenttype.folder.folder.IFolder>]

The instanciation provides a fully functionnal folderish object::

    >>> from zope.container.interfaces import IContainer
    >>> folder = Folder(title=u"Some title")
    >>> IContainer.providedBy(folder)
    True

The `Folder` class inherits from the ``grokcore.content``
OrderedContainer: the keys of container are orderable (read mutable)::

    >>> from grokcore.content import OrderedContainer
    >>> isinstance(folder, OrderedContainer)
    True


Test in-situ
============

Setup the environment

    >>> from zope.component.hooks import getSite
    >>> root = getSite()

Create a Folder.

    >>> from menhir.contenttype.folder import Folder
    >>> root[u'folder'] = Folder()
    >>> folder = root.get(u'folder')

Create a dummy content type, so that we can put dummy content in the folder.

    >>> import dolmen.content as content
    >>> class Dummy(content.Content):
    ...     content.name("Dummy")
    ...     # content.icon("dummy.png")

Fill the folder with some dummies.

    >>> folder[u'books'] = Dummy(title=u"Books")
    >>> folder[u'films'] = Dummy(title=u"Films")
    >>> folder[u'music'] = Dummy(title=u"Music")

    >>> folder[u'subfolder'] = Folder(title=u"SubFolder")
    >>> folder[u'subfolder'][u'subfolder2'] = Folder(title=u'SubFolder Two')
    >>> folder[u'subfolder'][u'bogus'] = Dummy(title=u'Bogus') 
    >>> folder[u'subfolder'][u'subfolder2'][u'hocus'] = Dummy(title=u"hocus")

Verify the contents are correct.

    >>> dict([x for x in folder.items()])
    {u'films': <menhir.contenttype.folder.Dummy object at ...>,
     u'books': <menhir.contenttype.folder.Dummy object at ...>,
     u'music': <menhir.contenttype.folder.Dummy object at ...>,
     u'subfolder': <menhir.contenttype.folder.folder.Folder object at ...>}

Let's take a look at it from the browser's point-of-view.

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.component import getMultiAdapter
    >>> request = TestRequest()

    >>> view = getMultiAdapter((folder, request), name=folder.selected_view)
    >>> view.__class__.__name__
    'FolderListing'

    >>> view.update()
    >>> print view.render()
    <div class="folder-listing">
      <h1>Content of the folder</h1>
      <div><table class="listing sortable">
      <thead>
        <tr>
          <th>Title</th>
          <th>Modification date</th>
        </tr>
      </thead>
      <tbody>
        <tr class="even">
          <td><a href="http://127.0.0.1/folder/books">books</a></td>
          <td></td>
        </tr>
        <tr class="odd">
          <td><a href="http://127.0.0.1/folder/films">films</a></td>
          <td></td>
        </tr>
        <tr class="even">
          <td><a href="http://127.0.0.1/folder/music">music</a></td>
          <td></td>
        </tr>
        <tr class="odd">
          <td><img src="http://127.0.0.1/@@/menhir-contenttype-folder-folder-IFolder-icon.png" alt="Folder" width="16" height="16" border="0" /> <a href="http://127.0.0.1/folder/subfolder">SubFolder</a></td>
          <td></td>
        </tr>
      </tbody>
    </table></div>
    </div>

We should have a look at the default view (index) as well.

    >>> view = getMultiAdapter((folder, request), name='index')
    >>> view.__class__.__name__
    'SelectedView'

    >>> view.update()
    >>> print view.render()
    <div class="folder-listing">
      <h1>Content of the folder</h1>
      <div><table class="listing sortable">
      <thead>
        <tr>
          <th>Title</th>
          <th>Modification date</th>
        </tr>
      </thead>
      <tbody>
        <tr class="even">
          <td><a href="http://127.0.0.1/folder/books">books</a></td>
          <td></td>
        </tr>
        <tr class="odd">
          <td><a href="http://127.0.0.1/folder/films">films</a></td>
          <td></td>
        </tr>
        <tr class="even">
          <td><a href="http://127.0.0.1/folder/music">music</a></td>
          <td></td>
        </tr>
        <tr class="odd">
          <td><img src="http://127.0.0.1/@@/menhir-contenttype-folder-folder-IFolder-icon.png" alt="Folder" width="16" height="16" border="0" /> <a href="http://127.0.0.1/folder/subfolder">SubFolder</a></td>
          <td></td>
        </tr>
      </tbody>
    </table></div>
    </div>

Lastly, let's change the folder layout to the full rendering view
provided in this package.

    >>> folder.selected_view = u'compositeview'
    >>> view = getMultiAdapter((folder, request), name=folder.selected_view)
    >>> view.__class__.__name__
    'CompositeView'

    >>> view.update()
    >>> print view.content()
    <div class="composite-view">
      <h1></h1>
      <div class="composite-body sequence-block">
        <div><form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data">
      <h1>books</h1>
    </form>
    </div>
      </div>
      <div class="composite-body sequence-block">
        <div><form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data">
      <h1>films</h1>
    </form>
    </div>
      </div>
      <div class="composite-body sequence-block">
        <div><form action="http://127.0.0.1" method="post"
          enctype="multipart/form-data">
      <h1>music</h1>
    </form>
    </div>
      </div>
      <div class="composite-body sequence-block">
        <div><div class="folder-listing">
      <h1>Content of the folder</h1>
      <div><table class="listing sortable">
      <thead>
        <tr>
          <th>Title</th>
          <th>Modification date</th>
        </tr>
      </thead>
      <tbody>
        <tr class="even">
          <td><img src="http://127.0.0.1/@@/menhir-contenttype-folder-folder-IFolder-icon.png" alt="Folder" width="16" height="16" border="0" /> <a href="http://127.0.0.1/folder/subfolder/subfolder2">SubFolder Two</a></td>
          <td></td>
        </tr>
        <tr class="odd">
          <td><a href="http://127.0.0.1/folder/subfolder/bogus">bogus</a></td>
          <td></td>
        </tr>
      </tbody>
    </table></div>
    <BLANKLINE>
    </div>
    </div>
      </div>
    </div>
