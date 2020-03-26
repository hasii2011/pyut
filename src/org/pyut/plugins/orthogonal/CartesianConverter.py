
from logging import Logger
from logging import getLogger
from typing import Tuple

from org.pyut.ui.UmlFrame import DEFAULT_WIDTH
from org.pyut.ui.UmlFrame import A4_FACTOR

ScreenCoordinates = Tuple[int, int]

SCALE_FACTOR: float = 0.75
XC:           int   = int(DEFAULT_WIDTH / 2)          # Half the screen size
YC:           int   = int(DEFAULT_WIDTH / A4_FACTOR)  # Account for A4
PC_X:         int   = XC   # Center X in Cartesian
PC_Y:         int   = -YC  # Center Y in Cartesian


class CartesianConverter:

    clsLogger: Logger = getLogger(__name__)
    x = 0

    def __init__(self):

        self.logger: Logger = CartesianConverter.clsLogger

    @staticmethod
    def cartesianToScreen(cartesianX: int, cartesianY: int):
        """
        ... you need to find the equivalent Cartesian coordinates of the centre point Pc. A translate
        will bring Pc to the centre of the screen, and a scale will bring everything you want to see on the screen.

        You need to flip the sign of y so that y will go up instead. Convert the center of the screen in Cartesian
        coordinate to (Xc,Yc) in pixels, and S, scale to convert Cartesian to pixels.
        Usually, Xc and Yc are half of the screen size.

        Xs = Xc + (X-Pcx) * S
        Ys = Yc - (Y-Pcy) * S

        where (X,Y) in Cartesian
        is mapped to (Xs,Ys) in screen coordinates,
        Pcx and Pcy are the center of the screen in Cartesian coordinates,
        S is the scale factor from Cartesian to pixels.

        [Reference](https://www.physicsforums.com/threads/screen-coordinates-to-cartesian-coordinates.268633/)
        """
        xS: float = XC + (cartesianX - PC_X) * SCALE_FACTOR
        yS: float = YC - (cartesianY - PC_Y) * SCALE_FACTOR

        return int(xS), int(yS)
