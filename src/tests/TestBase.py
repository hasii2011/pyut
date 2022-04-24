
import json

import logging
import logging.config

from unittest import TestCase

from pkg_resources import resource_filename

from org.pyut.ogl.preferences.OglPreferences import OglPreferences

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:                   str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME:      str = 'tests.resources.testclass'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass.ozzee'
    RESOURCES_TEST_DATA_PACKAGE_NAME:         str = 'tests.resources.testdata'
    RESOURCES_TEST_IMAGES_PACKAGE_NAME:       str = 'tests.resources.testimages'

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """"""

        OglPreferences.determinePreferencesLocation()  # Side effect;  not a good move

        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName
