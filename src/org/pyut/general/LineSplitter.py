
from typing import List
from typing import Tuple

from wx import DC


class LineSplitter:
    """
    This class implements a text split algorithm.
    You provide text to the method to split and it returns
    a list of strings; The length of text for each string <= total width.

    Sample use:
        text:       str        = "Hi, how are you today ?"
        splitLines: List[str] = LineSplitter().split(text, dc, 12)
    """

    def split(self, text: str, dc: DC, textWidth: int) -> List[str]:
        """
        Split the `text` into lines that fit into `textWidth` pixels.

        Args:
            text:       The text to split
            dc:         Device Context
            textWidth:  The width of the text in pixels

        Returns:
            A list of strings that are no wider than the input pixel `width`
        """
        splitLines: List[str] = text.splitlines()
        newLines:   List[str] = []

        for line in splitLines:
            words:     List[str] = line.split()
            lineWidth: int       = 0
            newLine:   str       = ""
            for word in words:
                word: str = f'{word} '

                extentSize: Tuple[int, int] = dc.GetTextExtent(word)        # width, height
                wordWidth:  int             = extentSize[0]
                if lineWidth + wordWidth <= textWidth:
                    newLine = f'{newLine}{word}'
                    lineWidth += wordWidth
                else:
                    newLines.append(newLine[:-1])   # remove last space
                    newLine = word
                    lineWidth = wordWidth

            newLines.append(newLine[:-1])

        return newLines
