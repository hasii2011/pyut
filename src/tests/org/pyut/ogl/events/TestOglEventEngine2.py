
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App
from wx import Frame
from wx import ID_ANY

from org.pyut.miniogl.AttachmentLocation import AttachmentLocation
from org.pyut.miniogl.DiagramFrame import DiagramFrame
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.model.PyutClass import PyutClass
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.events.InvalidKeywordException import InvalidKeywordException
from tests.TestBase import TestBase

from org.pyut.ogl.events.OglEventEngine import OglEventEngine
from org.pyut.ogl.events.OglEventType import OglEventType
from tests.org.pyut.miniogl.TestMiniOglCommon import Point


class TestOglEventEngine2(TestBase):
    """
    This is a unit test for the above;  It differs from TestOglEventEngine in that that
    module is an interactive UI
    This unit test mainly verifies that improperly using an incorrect kwargs keyword
    appropriately fails
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglEventEngine2.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglEventEngine2.clsLogger
        self.app: App = App()
        #  Create frame
        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

        self._umlFrame: DiagramFrame = umlFrame

        self._eventEngine: OglEventEngine = OglEventEngine(listeningWindow=self._umlFrame)

    def tearDown(self):
        self.app.OnExit()
        del self.app
        del self._umlFrame
        del self._eventEngine

    def testIncorrectShapeToCutEventKeyword(self):

        pyutClass: PyutClass = PyutClass(name='OglTestClass')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)

        self.assertRaises(InvalidKeywordException, lambda: self._eventEngine.sendEvent(OglEventType.CutOglClass, shapeToCutBAD=oglClass))

    def testIncorrectRequestLollipopLocation(self):
        """
        """

        pyutClass: PyutClass = PyutClass(name='ClassRequestingLollipopLocation')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.RequestLollipopLocation, requestShapeBAD=oglClass))

    def testIncorrectSelectedShapeKeywordShape(self):

        pyutClass: PyutClass = PyutClass(name='TestShape')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.ShapeSelected, shapeBAD=oglClass, position=Point(100, 100)))

    def testIncorrectSelectedShapeKeywordPosition(self):
        pyutClass: PyutClass = PyutClass(name='TestShape')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.ShapeSelected, shape=oglClass, positionBad=Point(100, 100)))

    def testIncorrectCreateLollipopInterfaceKeywordImplementor(self):
        pyutClass:       PyutClass         = PyutClass(name='Implementor')
        implementor:     OglClass          = OglClass(pyutClass=pyutClass)
        attachmentPoint: SelectAnchorPoint = SelectAnchorPoint(x=100, y=100, attachmentPoint=AttachmentLocation.SOUTH, parent=implementor)

        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.CreateLollipopInterface, implementorBAD=implementor,
                                                              attachmentPoint=attachmentPoint))

    def testIncorrectCreateLollipopInterfaceKeywordAttachmentPoint(self):
        pyutClass:       PyutClass         = PyutClass(name='Implementor')
        implementor:     OglClass          = OglClass(pyutClass=pyutClass)
        attachmentPoint: SelectAnchorPoint = SelectAnchorPoint(x=100, y=100, attachmentPoint=AttachmentLocation.SOUTH, parent=implementor)

        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.CreateLollipopInterface, implementor=implementor,
                                                              attachmentPointBAD=attachmentPoint))


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglEventEngine2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
