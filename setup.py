"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['src/Pyut.py']
DATA_FILES = [('org/pyut/resources', ['src/org/pyut/resources/loggingConfiguration.json']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kilroy-Pyut.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Help.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/Kudos.txt']),
              ('org/pyut/resources', ['src/org/pyut/resources/tips.txt']),

              ('org/pyut/resources/img', ['src/org/pyut/resources/img/pyut.ico']),


              ]
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    packages=['org',
              'org.pyut',
              'org.pyut.commands',
              'org.pyut.dialogs', 'org.pyut.dialogs.preferences', 'org.pyut.dialogs.tips',
              'org.pyut.enums',
              'org.pyut.errorcontroller',
              'org.pyut.experimental',
              'org.pyut.general', 'org.pyut.general.exceptions',
              'org.pyut.history',
              'org.pyut.miniogl',
              'org.pyut.model',
              'org.pyut.ogl', 'org.pyut.ogl.sd',
              'org.pyut.persistence', 'org.pyut.persistence.converters',
              'org.pyut.plugins',
              'org.pyut.plugins.base',
              'org.pyut.plugins.common',
              'org.pyut.plugins.dtd',
              'org.pyut.plugins.fastedit',
              'org.pyut.plugins.gml',
              'org.pyut.plugins.io',
              'org.pyut.plugins.iopythonsupport',
              'org.pyut.plugins.orthogonal',
              'org.pyut.plugins.sugiyama',
              'org.pyut.plugins.tools',
              'org.pyut.plugins.xmi',
              'org.pyut.plugins.xsd',
              'org.pyut.resources', 'org.pyut.resources.img', 'org.pyut.resources.img.methodparameters', 'org.pyut.resources.img.splash',
              'org.pyut.resources.img.toolbar', 'org.pyut.resources.locale',
              'org.pyut.ui', 'org.pyut.ui.tools'
              ],
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},

    url='https://github.com/hasii2011/PyUt',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='The Python UML Tool',
    options={},
    setup_requires=['py2app'],
    install_requires=['antlr4-python3-runtime',
                      'fpdf2',
                      'networkx',
                      'orthogonal',
                      'pygmlparser',
                      'pyumldiagrams',
                      'wxPython',
                      'xmlschema',
                      ]
)
