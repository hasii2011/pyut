from wx import CommandEvent

from pyut.errorcontroller.ErrorManager import ErrorManager
from pyut.errorcontroller.ErrorViewType import ErrorViewType


class DebugErrorViews:

    # noinspection PyUnusedLocal
    @staticmethod
    def debugGraphicErrorView(commandEvent: CommandEvent):

        em: ErrorManager = ErrorManager()
        DebugErrorViews._makeCalls(em=em, viewType=ErrorViewType.GRAPHIC_ERROR_VIEW)

    # noinspection PyUnusedLocal
    @staticmethod
    def debugTextErrorView(commandEvent: CommandEvent):

        em: ErrorManager = ErrorManager()
        DebugErrorViews._makeCalls(em=em, viewType=ErrorViewType.TEXT_ERROR_VIEW)

    # noinspection PyUnusedLocal
    @staticmethod
    def debugRaiseErrorView(commandEvent: CommandEvent):

        em: ErrorManager = ErrorManager()
        DebugErrorViews._makeCalls(em=em, viewType=ErrorViewType.RAISE_ERROR_VIEW)

    @staticmethod
    def _makeCalls(em: ErrorManager, viewType: ErrorViewType):

        em.errorViewType = viewType

        em.displayInformation(msg=f'{viewType} Message', title=f'{viewType} Title', parent=None)
        em.displayWarning(msg=f'{viewType} - Warning Message', title=f'{viewType} - WarningTitle', parent=None)
        em.displayFatalError(msg=f'{viewType}: Fatal Message', title=f'{viewType} - Fatal Title', parent=None)
