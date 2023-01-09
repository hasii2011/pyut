
from wx import CommandEvent

from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from wx import Window

from pyut.dialogs.BaseEditParamFieldDialog import BaseEditParamFieldDialog


class DlgEditParameter(BaseEditParamFieldDialog):

    def __init__(self, parent: Window, parameterToEdit: PyutParameter):
        """
        The Dialog to edit PyutParameters
        Args:
            parent:
            parameterToEdit:  The parameter that is being edited
        """
        super().__init__(parent, title="Edit Parameter", layoutField=False)

        self._parameterToEdit: PyutParameter = parameterToEdit

        self._name.SetValue(self._parameterToEdit.name)
        paramType: PyutType = self._parameterToEdit.type
        self._type.SetValue(paramType.value)
        self._defaultValue.SetValue(self._convertNone(self._parameterToEdit.defaultValue))

        self._name.SetFocus()
        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

    # noinspection PyUnusedLocal
    def _onOk (self, event: CommandEvent):
        """
        Add additional behavior to super class method
        Args:
            event:
        """

        nameValue: str = self._name.GetValue()
        if nameValue == '':
            self._indicateEmptyName()
            return

        self._parameterToEdit.name = nameValue
        paramType: PyutType = PyutType(self._type.GetValue())
        self._parameterToEdit.type = paramType
        if self._defaultValue.GetValue() != "":
            self._parameterToEdit.defaultValue = self._defaultValue.GetValue()
        else:
            self._parameterToEdit.defaultValue = ''

        super()._onOk(event)
