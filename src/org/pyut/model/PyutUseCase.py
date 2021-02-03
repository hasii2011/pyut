
from org.pyut.model.PyutLinkedObject import PyutLinkedObject
from org.pyut.preferences.PyutPreferences import PyutPreferences


class PyutUseCase(PyutLinkedObject):
    """
    """
    def __init__(self, name: str = ''):

        if name is None or name == '':
            name = PyutPreferences().useCaseName

        super().__init__(name)
