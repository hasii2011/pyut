

from wx import Printout
from wx import DC


class PyutPrintout(Printout):
    """
    Class to prepare for printing

    This class is used to prepare printing
    it's copying from wx.Python documentation

    :version: $Revision: 1.8 $
    :author:  Deve Roux
    :contact: droux@eivd.ch
    """
    def __init__(self, canvas):

        super().__init__()

        self.canvas = canvas
        self.nbPages = 1

    def HasPage(self, page):
        return page <= self.nbPages

    def GetPageInfo(self):
        return 1, self.nbPages, 1, self.nbPages

    def OnPrintPage(self, page):
        """
        Called by printing method

        @since 1.19
        @author Deve Roux <droux@eivd.ch>
        """
        dc: DC = self.GetDC()

        maxX = self.canvas.getWidth()
        maxY = self.canvas.getHeight()

        # Let's have at least 50 device units margin
        marginX = 50
        marginY = 50

        # Add the margin to the graphic size
        maxX = maxX + (2 * marginX)
        maxY = maxY + (2 * marginY)

        # Get the size of the DC in pixels
        # (w, h) = dc.GetSizeTuple()
        (w, h) = dc.GetSize()
        # Calculate a suitable scaling factor
        scaleX = float(w) / maxX
        scaleY = float(h) / maxY

        # Use x or y scaling factor, whichever fits on the DC
        actualScale = min(scaleX, scaleY)

        # Calculate the position on the DC for centring the graphic
        posX = (w - (self.canvas.getWidth() * actualScale)) / 2.0
        posY = (h - (self.canvas.getHeight() * actualScale)) / 2.0

        # Set the scale and origin
        dc.SetUserScale(actualScale, actualScale)
        dc.SetDeviceOrigin(int(posX), int(posY))

        self.canvas.Redraw(dc)
        return True
