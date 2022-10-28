"""
"""

from setuptools import setup

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['src/org/pyut/PyutV2.py']
DATA_FILES = [('org/pyut/resources', ['src/org/pyut/resources/loggingConfiguration.json']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kilroy-Pyut.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Help.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kudos.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/tips.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/version.txt']),

              ('org/pyut/resources/img', ['src/org/pyut/resources/img/pyut.ico']),
              ]
OPTIONS = {}

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name='Pyut',
    version='6.8.1',
    app=APP,
    data_files=DATA_FILES,
    packages=[
              'org',
              'org.pyut',
              'org.pyut.dialogs', 'org.pyut.dialogs.preferences', 'org.pyut.dialogs.preferences.valuecontainers',
              'org.pyut.dialogs.textdialogs',
              'org.pyut.dialogs.tips',
              'org.pyut.enums',
              'org.pyut.errorcontroller',
              'org.pyut.experimental',
              'org.pyut.general', 'org.pyut.general.datatypes', 'org.pyut.general.exceptions',
              'org.pyut.history', 'org.pyut.history.commands',
              'org.pyut.persistence', 'org.pyut.persistence.converters',
              'org.pyut.preferences',
              'org.pyut.resources',
              'org.pyut.resources.img',
              'org.pyut.resources.img.methodparameters',
              'org.pyut.resources.img.splash',
              'org.pyut.resources.img.toolbar', 'org.pyut.resources.img.toolbar.embedded16', 'org.pyut.resources.img.toolbar.embedded32',
              'org.pyut.resources.locale',
              'org.pyut.ui',   'org.pyut.ui.frame', 'org.pyut.ui.tools', 'org.pyut.ui.umlframes', 'org.pyut.ui.widgets',
              'org.pyut.uiv2', 'org.pyut.uiv2.eventengine'
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
            CFBundleIdentifier='org.pyut',
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
                      'PyGithub==1.55',
                      'wxPython==4.2.0',
                      'pyutmodel==1.1.0',
                      'ogl==0.60.5',
                      'oglio==0.5.7'
                      'pyutplugincore==0.5.10',
                      ]
)
