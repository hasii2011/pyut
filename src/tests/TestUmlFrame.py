
from typing import cast

import unittest

from os import getcwd
# from os import remove as osRemove

from wx import App
from wx import Frame
from wx import ID_ANY

from pyut.PyutUtils import PyutUtils
from pyut.errorcontroller.ErrorManager import ErrorManager

# from pyut.history.HistoryUtils import HISTORY_FILE_NAME

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.umlframes.UmlFrame import UmlFrame

from pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes

from pyut.uiv2.eventengine.EventEngine import EventEngine


class PyUtApp(App):
    def OnInit(self):
        return True


class TestUmlFrame(unittest.TestCase):
    """
    This class do basic tests on UmlFrame :
    it creates classes, actors, notes, links, etc...
    """

    clsFrame: UmlFrame = cast(UmlFrame, None)

    @classmethod
    def setUpClass(cls):

        PyutPreferences.determinePreferencesLocation()  # Side effect;  not a good move

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """
        """
        errorManager: ErrorManager = ErrorManager()
        errorManager.changeType(ErrorViewTypes.RAISE_ERROR_VIEW)

        whereWeAre: str = getcwd()
        PyutUtils.setBasePath(whereWeAre)

        self.app: App = App()
        #  Create frame
        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = UmlFrame(baseFrame, EventEngine(listeningWindow=baseFrame))
        umlFrame.Show(True)

        self._umlFrame: UmlFrame = umlFrame

    def tearDown(self):

        self.app.OnExit()

        del self.app
        del self._umlFrame
        # TODO remove new .json files
        # for x in range(4):
        #
        #     try:
        #         osRemove(f'{HISTORY_FILE_NAME}{x}')
        #     except (ValueError, Exception):
        #         pass    # we truly want to ignore

    def testPlaceHolder(self):
        pass


def suite() -> unittest.TestSuite:

    import unittest

    testSuite: unittest.TestSuite = unittest.TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUmlFrame))

    return testSuite


if __name__ == '__main__':
    unittest.main()
