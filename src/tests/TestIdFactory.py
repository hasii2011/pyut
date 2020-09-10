
from typing import List
from typing import Set

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutUseCase import PyutUseCase

from tests.TestBase import TestBase

from org.pyut.persistence.converters.IDFactorySingleton import IDFactory


class TestIDFactory(TestBase):
    """
    Tests the newly refactored IDFactory that is a Singleton
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestIDFactory.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestIDFactory.clsLogger

    def tearDown(self):
        pass

    def testBasicIDGeneration(self):
        idFactory: IDFactory = IDFactory()

        pyutClassId: int = idFactory.getID(PyutClass)
        pyutFieldId: int = idFactory.getID(PyutField)

        self.assertNotEqual(pyutClassId, pyutFieldId, 'ID generator is failing')

    def testBasicIDCaching(self):

        idFactory: IDFactory = IDFactory()

        pyutClassId:  int = idFactory.getID(PyutClass)
        pyutClassId2: int = idFactory.getID(PyutClass)
        self.assertEqual(pyutClassId, pyutClassId2, 'ID generator is not caching')

    def testLengthierGeneration(self):

        idFactory: IDFactory = IDFactory()

        longerClassList: List[type] = [
            PyutMethod,
            PyutUseCase,
            PyutActor,
            PyutNote,
            PyutLink
        ]
        knownIds: Set[int] = set()

        for cls in longerClassList:
            clsID: int = idFactory.getID(cls)
            if clsID in knownIds:
                self.fail('')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestIDFactory))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
