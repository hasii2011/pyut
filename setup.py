"""
"""

from setuptools import setup

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['src/pyut/PyutV2.py']
DATA_FILES = [('pyut/resources', ['src/pyut/resources/loggingConfiguration.json']),
              ('pyut/resources', ['src/pyut/resources/Kilroy-Pyut.txt']),
              ('pyut/resources', ['src/pyut/resources/Help.txt']),
              ('pyut/resources', ['src/pyut/resources/Kudos.txt']),
              ('pyut/resources', ['src/pyut/resources/tips.txt']),
              ('pyut/resources', ['src/pyut/resources/version.txt']),

              ('pyut/resources/img', ['src/pyut/resources/img/pyut.ico']),
              ]
OPTIONS = {}

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name='Pyut',
    version='7.6.0',
    app=APP,
    data_files=DATA_FILES,
    packages=[
              'pyut',
              'pyut.dialogs', 'pyut.dialogs.preferencesv2', 'pyut.dialogs.preferencesv2.valuecontrols',
              'pyut.dialogs.textdialogs',
              'pyut.dialogs.tips',
              'pyut.enums',
              'pyut.errorcontroller',
              'pyut.experimental',
              'pyut.general', 'pyut.general.datatypes', 'pyut.general.exceptions',
              'pyut.preferences',
              'pyut.resources',
              'pyut.resources.img',
              'pyut.resources.img.methodparameters',
              'pyut.resources.img.splash',
              'pyut.resources.img.toolbar', 'pyut.resources.img.toolbar.embedded16', 'pyut.resources.img.toolbar.embedded32',
              'pyut.resources.locale',
              'pyut.ui',   'pyut.ui.frame', 'pyut.ui.tools', 'pyut.ui.umlframes', 'pyut.ui.widgets', 'pyut.ui.wxcommands',
              'pyut.uiv2', 'pyut.uiv2.eventengine', 'pyut.uiv2.eventengine.eventinformation'
              ],
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},

    url='https://github.com/hasii2011/PyUt',
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
                {'CFBundleTypeName': 'Pyut'},
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
                      'PyGithub==1.57',
                      'wxPython==4.2.0',
                      'pyutmodel==1.3.4',
                      'ogl~=0.60.30',
                      'oglio~=0.5.50',
                      'pyutplugins~=0.6.9',
                      ]
)
