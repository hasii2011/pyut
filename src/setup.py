
import pathlib
from setuptools import setup
from setuptools import find_packages
from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
APP = ['Sandwich.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    name="pyut",
    version="3.0",
    description="Python UML Tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://hasii2011.github.io",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["wxPython"],
    setup_requires=['py2app'],
)
