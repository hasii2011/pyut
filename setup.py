
from setuptools import setup

import pathlib

from pyut import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['pyut/PyutV2.py']
DATA_FILES = [('pyut/resources', ['pyut/resources/loggingConfiguration.json']),
              ('pyut/resources', ['pyut/resources/Kilroy-Pyut.txt']),
              ('pyut/resources', ['pyut/resources/Help.txt']),
              ('pyut/resources', ['pyut/resources/Kudos.txt']),
              ('pyut/resources', ['pyut/resources/tips.txt']),
              ('pyut/resources/img', ['pyut/resources/img/pyut.ico']),
              ]
OPTIONS = {}

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name='Pyut',
    version=__version__,
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
    long_description='A UML Diagrammer with plugin support and reverse engineering capabilities.',
    options=dict(py2app=dict(
        plist=dict(
            NSRequiresAquaSystemAppearance='True',
            CFBundleGetInfoString='Edits Pyut UML Files',
            CFBundleIdentifier='pyut',
            CFBundleShortVersionString=__version__,
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
            LSMultipleInstancesProhibited='True',
        )
    ),
    ),
    setup_requires=['py2app'],
    install_requires=['pyutmodelv2==2.0.0a7',
                      'ogl==2.0.0a7',
                      'oglio==2.0.0a7',
                      'pyutplugins==2.0.0a11',
                      'codeallybasic~=0.5.2',
                      'codeallyadvanced~=0.5.2',
                      'PyGithub==1.59.1',
                      'wxPython==4.2.1',
                      'chardet==5.2.0'
                      ]
)
