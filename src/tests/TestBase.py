
import os
import json
import logging
import logging.config

from unittest import TestCase

JSON_LOGGING_CONFIG_FILENAME = "testLoggingConfig.json"


class TestBase(TestCase):
    """
    A base unit test class to initialize some logging stuff we need
    """

    @classmethod
    def setUpLogging(cls):
        """"""
        cls.findLoggingConfig()

        with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls):
        """"""
        if os.path.isfile(JSON_LOGGING_CONFIG_FILENAME):
            return
        else:
            os.chdir("../")
            cls.findLoggingConfig()
