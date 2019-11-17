
from typing import List

from wx import DC


class LineSplitter:
    """
    This class offers a text split algorithm.
    You can give your text to the method split and this will return you
    a list of string, length of text for each string <= total width.

    Sample of use::
        text = "Hi, how are you today ?"
        splitLines = LineSplitter().split(text, dc, 12)
    """

    def split(self, text: str, dc: DC, width: int) -> List[str]:
        """
        Split a text in lines fitting in width pixels.

        @param  text : text to split
        @param  dc
        @param  width : width for the text, in pixels

        @return String [] : a list of strings fitting in width pixels

        """
        lines = text.splitlines()
        newLines = []
        for line in lines:
            words = line.split()
            wline = 0
            newLine = ""
            for word in words:
                word += " "
                wword = dc.GetTextExtent(word)[0]
                if wline + wword <= width:
                    newLine += word
                    wline += wword
                else:
                    newLines.append(newLine[:-1])   # remove last space
                    newLine = word
                    wline = wword
            newLines.append(newLine[:-1])
        return newLines
