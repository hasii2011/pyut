
from setuptools import setup
from setuptools import find_packages

import pathlib

from pyut import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['pyut/Pyut.py']
DATA_FILES = [('pyut/resources', ['pyut/resources/loggingConfiguration.json']),
              ('pyut/resources', ['pyut/resources/Kilroy-Pyut.txt']),
              ('pyut/resources', ['pyut/resources/Help.txt']),
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
    packages=find_packages(include=['pyut.*']),
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
        'codeallybasic>=1.10.0',
        'codeallyadvanced>=1.4.2',
        'pyutmodelv2>=2.2.3',
        'ogl>=3.6.7',
        'oglio>=2.4.0',
        'pyutplugins>=3.2.6',
        'semantic-version==2.10.0',
        'PyGithub==2.6.1',
        'wxPython==4.2.2',
        'chardet==5.2.0'
    ]
)
