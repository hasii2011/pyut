"""
"""

from setuptools import setup

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['src/org/pyut/Pyut.py']
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
    version='6.7.0',
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
              'org.pyut.plugins',
              'org.pyut.plugins.base',
              'org.pyut.plugins.common',
              'org.pyut.plugins.dtd',
              'org.pyut.plugins.fastedit',
              'org.pyut.plugins.gml',
              'org.pyut.plugins.io',
              'org.pyut.plugins.io.javasupport',
              'org.pyut.plugins.io.nativeimagesupport',
              'org.pyut.plugins.io.pyumlsupport',
              'org.pyut.plugins.iopythonsupport', 'org.pyut.plugins.iopythonsupport.pyantlrparser',
              'org.pyut.plugins.orthogonal',
              'org.pyut.plugins.sugiyama',
              'org.pyut.plugins.tools',
              'org.pyut.plugins.xmi',
              'org.pyut.plugins.xsd',
              'org.pyut.preferences',
              'org.pyut.resources',
              'org.pyut.resources.img',
              'org.pyut.resources.img.methodparameters',
              'org.pyut.resources.img.splash',
              'org.pyut.resources.img.toolbar', 'org.pyut.resources.img.toolbar.embedded16', 'org.pyut.resources.img.toolbar.embedded32',
              'org.pyut.resources.locale',
              'org.pyut.ui', 'org.pyut.ui.frame', 'org.pyut.ui.tools', 'org.pyut.ui.widgets'
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
    license=LICENSE,
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
    install_requires=['antlr4-python3-runtime',
                      'orthogonal==1.1.6',
                      'pygmlparser==1.0.1',
                      'pyumldiagrams==2.30.6',
                      'PyGithub==1.55',
                      'wxPython==4.1.1',
                      'xmlschema==1.11.1',
                      'pyutmodel==1.0.4',
                      'ogl==0.53.5',
                      ]
)
