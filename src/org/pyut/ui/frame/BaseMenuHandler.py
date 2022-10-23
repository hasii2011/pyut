from typing import Optional

from wx import Menu
from wx import Window

# from org.pyut.ui.Mediator import Mediator
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class BaseMenuHandler:

    def __init__(self, menu: Menu, eventEngine: Optional[IEventEngine]):

        self._menu:        Menu         = menu
        self._eventEngine: IEventEngine = eventEngine              # type: ignore
        # self._mediator:    Mediator     = Mediator()               # TODO: We will obviate the need for this
        self._parent:      Window       = self._menu.GetWindow()   # TODO this does not work at init
