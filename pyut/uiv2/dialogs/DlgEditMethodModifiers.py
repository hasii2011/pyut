
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ID_ANY

from wx import CommandEvent

from wx.adv import EL_ALLOW_DELETE
from wx.adv import EL_ALLOW_EDIT
from wx.adv import EL_ALLOW_NEW
from wx.adv import EL_DEFAULT_STYLE
from wx.adv import EditableListBox

from wx.lib.sized_controls import SizedPanel

from pyutmodelv2.PyutMethod import PyutModifiers
from pyutmodelv2.PyutModifier import PyutModifier

from pyut.uiv2.dialogs.BaseEditDialog import BaseEditDialog


class DlgEditMethodModifiers(BaseEditDialog):

    def __init__(self, parent, pyutModifiers: PyutModifiers):

        super().__init__(parent, title='Edit Method Modifiers')

        self.logger:             Logger        = getLogger(__name__)
        self._pyutModifiers:     PyutModifiers = pyutModifiers
        self._pyutModifiersCopy: PyutModifiers = deepcopy(pyutModifiers)

        self._elb: EditableListBox = cast(EditableListBox, None)
        sizedPanel: SizedPanel = self.GetContentsPane()

        self._layoutEditableListBox(sizedPanel)
        self._layoutStandardOkCancelButtonSizer()

    @property
    def pyutModifiers(self) -> PyutModifiers:
        return self._stringToPyutModifiers()

    def _layoutEditableListBox(self, parent: SizedPanel):
        style: int = EL_DEFAULT_STYLE | EL_ALLOW_NEW | EL_ALLOW_EDIT | EL_ALLOW_DELETE
        self._elb = EditableListBox(parent, ID_ANY, "Modifiers", (-1, -1), (-1, -1), style=style)

        self._elb.SetStrings(self._pyutModifiersToStrings())

    def _onOk(self, event: CommandEvent):
        """
        """

        super()._onOk(event)

    def _pyutModifiersToStrings(self) -> List[str]:
        """
        Converts the modifiers copy to a list of string
        Returns:
        """

        stringList: List[str] = []
        for modifier in self._pyutModifiersCopy:
            pyutModifier: PyutModifier = cast(PyutModifier, modifier)
            stringList.append(pyutModifier.name)

        return stringList

    def _stringToPyutModifiers(self) -> PyutModifiers:
        pyutModifiers: PyutModifiers = PyutModifiers([])
        strList:       List[str]     = self._elb.GetStrings()
        for modifierString in strList:
            pyutModifier: PyutModifier = PyutModifier(name=modifierString)
            pyutModifiers.append(pyutModifier)

        return pyutModifiers
