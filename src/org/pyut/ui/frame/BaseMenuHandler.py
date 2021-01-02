
from wx import Menu
from wx import Window

from org.pyut.general.Mediator import Mediator


class BaseMenuHandler:

    def __init__(self, menu: Menu):

        self._menu:     Menu     = menu
        self._mediator: Mediator = Mediator()
        self._parent:   Window   = self._menu.GetWindow()   # TODO this does not work at init
