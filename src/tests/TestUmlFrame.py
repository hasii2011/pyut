

import unittest
from os import getcwd
from os import remove as osRemove

from wx import App
from wx import Frame
from wx import ID_ANY

from org.pyut.PyutUtils import PyutUtils
from org.pyut.errorcontroller.ErrorManager import ErrorManager

from org.pyut.history.HistoryUtils import HISTORY_FILE_NAME

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.UmlFrame import UmlFrame
from org.pyut.ui.TreeNotebookHandler import TreeNotebookHandler

from org.pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from org.pyut.general.Mediator import Mediator


class PyUtApp(App):
    def OnInit(self):
        return True


class TestUmlFrame(unittest.TestCase):
    """
    This class do basic tests on UmlFrame :
    it creates classes, actors, notes, links, etc...
    @author C.Dutoit
    """

    def setUp(self):
        """

        """
        PyutPreferences.determinePreferencesLocation()  # Side effect;  not a good move

        # Initialize mediator and error manager
        mediator: Mediator = Mediator()
        mediator.setScriptMode()

        fileHandling: TreeNotebookHandler = TreeNotebookHandler(None)
        mediator.registerFileHandling(fileHandling)

        errorManager: ErrorManager = mediator.getErrorManager()
        errorManager.changeType(ErrorViewTypes.RAISE_ERROR_VIEW)

        whereWeAre: str = getcwd()
        PyutUtils.setBasePath(whereWeAre)

        # Create wx application
        # For python 3 and wx 4.x we need to save it so it does not get garbage collected
        self.app: App = App()

        #  Create frame
        baseFrame = Frame(None, ID_ANY, "", size=(10, 10))
        umlFrame = UmlFrame(baseFrame, None)
        umlFrame.Show(True)
        self._umlFrame = umlFrame

    def tearDown(self):

        del self.app
        del self._umlFrame
        for x in range(4):

            try:
                osRemove(f'{HISTORY_FILE_NAME}{x}')
            except (ValueError, Exception):
                pass    # we truly want to ignore

    def testClassCreation(self):
        """
        Test Class Creation
        @author C.Dutoit
        """
        # Create a PyutClass
        try:
            pyutClass = self._umlFrame.createNewClass(10, 10)
        except (ValueError, Exception) as e:
            self.fail(f"Can't create a PyutClass: {e}")

        # Get the corresponding OglClass
        try:
            oglClass = [s for s in self._umlFrame.getDiagram().GetShapes() if s.getPyutObject() is pyutClass][0]  # Too cute; fix
        except (ValueError, Exception):
            self.fail("Can't get OglClass")

        # Testing position
        try:
            x, y = oglClass.GetPosition()
        except (ValueError, Exception):
            self.fail("Can't get OglClass position")
        self.assertTrue(x == 10 and y == 10, "Wrong OglClass position !")

    def testNoteCreation(self):
        """
        Test Note Creation
        @author C.Dutoit
        """
        # PyutNote creation
        try:
            pyutNote = self._umlFrame.createNewNote(100, 10)
        except (ValueError, Exception):
            self.fail("Can't create a PyutNote")

        # Get OglNote
        try:
            oglNote = [s for s in self._umlFrame.getDiagram().GetShapes() if s.getPyutObject() is pyutNote][0]  # Too cute; fix
        except (ValueError, Exception):
            self.fail("Can't get OglNote")

        # Testing position
        try:
            x, y = oglNote.GetPosition()
        except (ValueError, Exception):
            self.fail("Can't get OglNote position")
        self.assertTrue(x == 100 and y == 10, "Wrong OglNote position !")

    def testActorCreation(self):
        """
        Test Actor Creation
        @author C.Dutoit
        """
        # Create a PyutActor
        try:
            pyutActor = self._umlFrame.createNewActor(100, 100)
        except (ValueError, Exception):
            self.fail("Can't create a PyutActor")

        # Get the corresponding OglActor
        try:
            oglActor = [s for s in self._umlFrame.getDiagram().GetShapes() if s.getPyutObject() is pyutActor][0]  # Too cute; fix
        except (ValueError, Exception):
            self.fail("Can't get OglActor")

        # Testing position
        try:
            x, y = oglActor.GetPosition()
        except (ValueError, Exception):
            self.fail("Can't get OglActor position")
        self.assertTrue(x == 100 and y == 100, "Wrong OglActor position !")

    def testUseCaseCreation(self):
        """
        Test UseCase Creation
        @author C.Dutoit
        """
        # Create a PyutUseCase
        try:
            pyutUseCase = self._umlFrame.createNewUseCase(10, 50)
        except (ValueError, Exception):
            self.fail("Can't create a PyutUseCase")

        # Get the corresponding OglUseCase
        try:
            oglUseCase = [s for s in self._umlFrame.getDiagram().GetShapes() if s.getPyutObject() is pyutUseCase][0]  # Too cute; fix
        except (ValueError, Exception):
            self.fail("Can't get OglUseCase")

        # Testing position
        try:
            x, y = oglUseCase.GetPosition()
        except (ValueError, Exception):
            self.fail("Can't get OglUseCase position")
        self.assertTrue(x == 10 and y == 50, "Wrong OglUseCase position !")

    # def testInheritanceLinkCreation(self):
    #     """
    #     Test Inheritance link Creation
    #     @author C.Dutoit
    #     """
    #     # Create two PyutClass
    #     try:
    #         pyutClass1 = self._umlFrame.createNewClass(20, 10)
    #         pyutClass2 = self._umlFrame.createNewClass(30, 10)
    #     except (ValueError, Exception) as e:
    #         self.fail(f"Can't create two PyutClass;  {e}")
    #
    #     # Get OglObject
    #     try:
    #         oglClass1 = [s for s in self._umlFrame.getDiagram().GetShapes()
    #                        if s.getPyutObject() is pyutClass1][0]
    #         oglClass2 = [s for s in self._umlFrame.getDiagram().GetShapes()
    #                        if s.getPyutObject() is  pyutClass2][0]
    #     except (ValueError, Exception) as e:
    #         self.fail(f"Can't get the two OglClass;  {e}")
    #
    #     # Create the link
    #     try:
    #         self._umlFrame.createInheritanceLink(oglClass1, oglClass2)
    #     except (ValueError, Exception) as e:
    #         self.fail(f"Can't create a inheritance link;  {e}")

    # def testNewLinkCreation(self):
    #     """
    #     Test new link Creation
    #     @author C.Dutoit
    #     """
    #     # Create two PyutClass
    #     try:
    #         pyutClass1 = self._umlFrame.createNewClass(20, 20)
    #         pyutClass2 = self._umlFrame.createNewClass(30, 20)
    #     except (ValueError, Exception):
    #         self.fail("Can't create two PyutClass")
    #
    #     # Get OglObject
    #     try:
    #         oglClass1 = [s for s in self._umlFrame.getDiagram().GetShapes()
    #                        if s.getPyutObject() is pyutClass1][0]
    #         oglClass2 = [s for s in self._umlFrame.getDiagram().GetShapes()
    #                        if s.getPyutObject() is  pyutClass2][0]
    #     except (ValueError, Exception):
    #         self.fail("Can't get the two OglClass")
    #
    #     # Create the link
    #     try:
    #         self._umlFrame.createNewLink(oglClass1, oglClass2)
    #     except (ValueError, Exception):
    #         self.fail("Can't create a new link")


def suite() -> unittest.TestSuite:

    import unittest

    testSuite: unittest.TestSuite = unittest.TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUmlFrame))

    return testSuite


if __name__ == '__main__':
    unittest.main()
