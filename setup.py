# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'menhir.contenttype.privatefolder'
version = '0.1'
readme = open(join('src', 'menhir', 'contenttype',
                   'privatefolder', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

tests_require = [
    'dolmen.app.security',
    'grokcore.content',
    'zope.component',
    'zope.container',
    'zope.location',
    'zope.principalregistry',
    'zope.publisher',
    'zope.security',
    'zope.securitypolicy',
    'zope.site',
    'zope.traversing',
    ]

setup(name = name,
      version = version,
      description = 'Dolmen contenttype extension : private folder',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'souheil@chelfouh.com',
      url = 'http://www.dolmen-project.org/',
      download_url = '',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['menhir', 'menhir.contenttype'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      install_requires=[
          'dolmen.app.container >= 1.0b2',
          'dolmen.app.content >= 1.0b1',
          'dolmen.app.layout',
          'dolmen.app.viewselector',
          'dolmen.content >= 0.7',
          'dolmen.menu',
          'grokcore.view',
          'setuptools',
          'zope.component',
          'zope.i18n',
          'zope.i18nmessageid',
      ],
      classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
