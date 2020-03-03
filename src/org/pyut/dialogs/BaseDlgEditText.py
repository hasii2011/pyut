
from logging import Logger
from logging import getLogger

from wx import CAPTION
from wx import Dialog
from wx import RESIZE_BORDER
from wx import Window


class BaseDlgEditText(Dialog):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window, dialogIdentifier: int, dialogTitle: str):

        super().__init__(parent, dialogIdentifier, dialogTitle, style=RESIZE_BORDER | CAPTION)

        self._returnAction: int = -1   # describe how the user exited the dialog box
