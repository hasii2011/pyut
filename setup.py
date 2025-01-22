
from setuptools import setup

import pathlib

from pyut import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['pyut/Pyut.py']
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
        'pyut.ui',
        'pyut.ui.dialogs', 'pyut.ui.dialogs.preferences', 'pyut.ui.dialogs.textdialogs', 'pyut.ui.dialogs.tips',
        'pyut.ui.eventengine', 'pyut.ui.eventengine.eventinformation', 'pyut.ui.eventengine.inspector',
        'pyut.ui.main',
        'pyut.ui.menuhandlers',
        'pyut.ui.tools',
        'pyut.ui.umlframes', 'pyut.ui.wxcommands',
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
            NSRequiresAquaSystemAppearance='False',
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
    install_requires=[
        'codeallybasic>=1.9.0',
        'codeallyadvanced>=1.3.3',
        'pyutmodelv2>=2.2.0',
        'ogl>=3.6.3',
        'oglio>=2.3.4',
        'pyutplugins>=3.2.3',
        'semantic-version==2.10.0',
        'PyGithub==2.4.0',
        'wxPython==4.2.2',
        'chardet==5.2.0'
    ]
)
