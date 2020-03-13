from typing import Dict
from typing import List
from typing import TextIO
from typing import Pattern

from logging import Logger
from logging import getLogger

import re
from typing import Tuple


class FieldExtractor:

    def __init__(self, filename: str):

        self.logger: Logger = getLogger(__name__)
        self._filename = filename

    def getFields(self, className):

        regExVar:       Pattern = re.compile(r"^\s*self\.(.*)=(.*)")
        regExClass:     Pattern = re.compile(r"^\s*class\s+" + className.strip())
        regExNextClass: Pattern = re.compile(r"^\s*class\s+")
        regExMultiLine: Pattern = re.compile(r"\\s*$")

        lines: List[str] = self._getTheSourceCode()

        foundFields: Dict[str, str] = {}
        inClass:     bool = False
        buffer:      str = ""
        multiLine:   bool = False
        for line in lines:
            # skip other classes in the same file
            # TODO : beware, this will interrupt if there's an inner class !!!
            if not inClass:
                if regExClass.search(line):
                    inClass = True
                else:
                    continue
            else:
                if regExNextClass.search(line):
                    break
            if multiLine:
                line = buffer + line.strip()
            if regExMultiLine.search(line):
                buffer = line[:line.rindex("\\")]
                self.logger.info(f'buffer = {buffer}')
                multiLine = True
                continue
            else:
                multiLine = False

            res: List[Tuple[str, str]] = regExVar.findall(line)
            if res:
                foundFields = self._cleanupField(foundFields, res)
        return foundFields

    def _cleanupField(self, foundFields, res):

        for name, initialValue in res:
            name: str = self._removeExtraneousNameParts(nameToClean=name)
            initialValue: str = self._removePart(initialValue, "#")

            if name not in foundFields:
                foundFields[name] = initialValue.strip()
                self.logger.debug(f'adding field: {repr(name.strip())}={initialValue.strip()}')

        return foundFields

    def _getTheSourceCode(self) -> List[str]:

        fd: TextIO = open(self._filename)
        lines: List[str] = fd.readlines()
        fd.close()

        return lines

    def _removeExtraneousNameParts(self, nameToClean: str) -> str:

        for charToRemove in ['.', '(', '[', '+', '-', '*', '/', '%']:
            nameToClean = self._removePart(nameToClean, charToRemove)

        nameToClean.strip()

        return nameToClean

    def _removePart(self, string: str, char: str):
        """

        Args:
            string:     String to update
            char:       Character to remove

        Returns:
            Updated string with char removed, if found
        """

        i = string.find(char)
        if i != -1:
            return string[:i]
        return string
