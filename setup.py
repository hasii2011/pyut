
from setuptools import setup

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['pyut/PyutV2.py']
DATA_FILES = [('pyut/resources', ['pyut/resources/loggingConfiguration.json']),
              ('pyut/resources', ['pyut/resources/Kilroy-Pyut.txt']),
              ('pyut/resources', ['pyut/resources/Help.txt']),
              ('pyut/resources', ['pyut/resources/Kudos.txt']),
              ('pyut/resources', ['pyut/resources/tips.txt']),
              ('pyut/resources', ['pyut/resources/version.txt']),

              ('pyut/resources/img', ['pyut/resources/img/pyut.ico']),
              ]
OPTIONS = {}

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()
VERSION = (HERE / 'pyut/resources/version.txt').read_text()

setup(
    name='Pyut',
    version=VERSION,
    app=APP,
    data_files=DATA_FILES,
    packages=[
              'pyut',
              'pyut.enums',
              'pyut.errorcontroller',
              'pyut.experimental',
              'pyut.general', 'pyut.general.datatypes', 'pyut.general.exceptions',
              'pyut.preferences',
              'pyut.resources',
              'pyut.resources.img',
              'pyut.resources.img.splash',
              'pyut.ui',   'pyut.ui.frame', 'pyut.ui.tools', 'pyut.ui.umlframes', 'pyut.ui.wxcommands',
              'pyut.uiv2', 'pyut.uiv2.eventengine', 'pyut.uiv2.eventengine.eventinformation',
              'pyut.uiv2.dialogs', 'pyut.uiv2.dialogs.preferencesv2',
              'pyut.uiv2.dialogs.textdialogs',
              'pyut.uiv2.dialogs.tips',
    ],
    include_package_data=True,
    zip_safe=False,

    url='https://github.com/hasii2011/pyut',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='The Python UML Tool',
    long_description=README,
    options=dict(py2app=dict(
        plist=dict(
            CFBundleGetInfoString='Edits Pyut UML Files',
            CFBundleIdentifier='pyut',
            CFBundleDocumentTypes=[
                {'CFBundleTypeName': 'pyut'},
                {'CFBundleTypeRole': 'Editor'},
                {'CFBundleTypeExtensions':  ['put', 'xml']}
            ],
            LSMinimumSystemVersion='12',
            LSEnvironment=dict(
                APP_MODE='True',
                PYTHONOPTIMIZE='1',
            ),
        )
    ),
    ),
    setup_requires=['py2app'],
    install_requires=[
                      'PyGithub==1.58.1',
                      'wxPython==4.2.0',
                      'hasiihelper~=0.2.0',
                      'pyutmodel==1.4.3',
                      'hasiicommon~=0.2.2',
                      'ogl~=0.70.26',
                      'oglio~=0.7.4',
                      'pyutplugins~=0.8.80',
                      ]
)
