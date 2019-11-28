from wx import CommandEvent

from org.pyut.errorcontroller.ErrorManager import getErrorManager
from org.pyut.errorcontroller.ErrorManager import ErrorManager
from org.pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes


class DebugErrorViews:

    # noinspection PyUnusedLocal
    @staticmethod
    def debugGraphicErrorView(commandEvent: CommandEvent):

        em: ErrorManager = getErrorManager()
        DebugErrorViews._makeCalls(em=em, viewType=ErrorViewTypes.GRAPHIC_ERROR_VIEW)

    # noinspection PyUnusedLocal
    @staticmethod
    def debugTextErrorView(commandEvent: CommandEvent):

        em: ErrorManager = getErrorManager()
        DebugErrorViews._makeCalls(em=em, viewType=ErrorViewTypes.TEXT_ERROR_VIEW)

    # noinspection PyUnusedLocal
    @staticmethod
    def debugRaiseErrorView(commandEvent: CommandEvent):

        em: ErrorManager = getErrorManager()
        DebugErrorViews._makeCalls(em=em, viewType=ErrorViewTypes.RAISE_ERROR_VIEW)

    @staticmethod
    def _makeCalls(em: ErrorManager, viewType: ErrorViewTypes):

        em.changeType(viewType)

        em.displayInformation(msg=f'{viewType} Message', title=f'{viewType} Title', parent=None)
        em.newWarning(msg=f'{viewType} - Warning Message', title=f'{viewType} - WarningTitle', parent=None)
        em.newFatalError(msg=f'{viewType}: Fatal Message', title=f'{viewType} - Fatal Title', parent=None)
