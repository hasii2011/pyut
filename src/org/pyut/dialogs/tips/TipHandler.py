
from typing import NewType
from typing import TextIO
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from org.pyut.preferences.PyutPreferences import PyutPreferences

TipLinesType = NewType('TipLinesType', List[str])


class TipHandler:
    """
    And I expect a 20% gratuity regardless of the kind of service I give you, if any
    """
    def __init__(self, fqFileName: str):
        """

        Args:
            fqFileName:  Fully qualified file name
        """
        self.logger: Logger          = getLogger(__name__)
        self._prefs: PyutPreferences = PyutPreferences()

        tipLines: TipLinesType = self._cacheTips(fileName=fqFileName)
        tipCount: int          = self._computeTipCount(tipLines=tipLines)

        self._tipLines: TipLinesType = tipLines
        self._tipCount: int          = tipCount

        self._currentTipNumber: int = self._safelyRetrieveCurrentTipNumber()

    @property
    def currentTipNumber(self) -> int:
        return self._currentTipNumber

    def getCurrentTipText(self) -> str:

        tipText: str = self._tipLines[self._currentTipNumber]

        self.logger.debug(f'{tipText=}')

        return tipText

    def incrementTipNumber(self, byValue: int):
        """
        Increment/Decrement.  Returns non-zero tip number

        Args:
            byValue:   Use negative number to decrement
        """
        tipNumber = (self._currentTipNumber + byValue) % self._tipCount
        if tipNumber < 0:
            tipNumber = self._tipCount

        self._currentTipNumber = tipNumber
        self.logger.info(f'{self._currentTipNumber=}')

    def _cacheTips(self, fileName: str) -> TipLinesType:

        file:     TextIO       = open(fileName)
        tipLines: TipLinesType = cast(TipLinesType, file.read().split(f'{osLineSep}'))
        file.close()

        return tipLines

    def _computeTipCount(self, tipLines: TipLinesType) -> int:
        return len(tipLines) - 1  # because we use it as a 0-based index

    def _safelyRetrieveCurrentTipNumber(self) -> int:

        currentTipNumber: int = self._prefs.currentTip
        if currentTipNumber is None:
            return 0
        else:
            return currentTipNumber
