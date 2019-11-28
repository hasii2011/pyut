from wx import CommandEvent

from org.pyut.errorcontroller.ErrorManager import getErrorManager
from org.pyut.errorcontroller.ErrorManager import ErrorManager
from org.pyut.errorcontroller.ErrorViewTypes import ErrorViewTypes


class DebugErrorViews:

    # noinspection PyUnusedLocal
    @staticmethod
    def debugGraphicView(commandEvent: CommandEvent):

        em: ErrorManager = getErrorManager()
        em.changeType(ErrorViewTypes.GRAPHIC_ERROR_VIEW)

        em.displayInformation(msg='Graphic Message', title='Graphic Title', parent=None)
        em.newWarning(msg='Warning Message', title='WarningTitle', parent=None)
        em.newFatalError(msg='Fatal Messafge', title='Fatal Title', parent=None)
