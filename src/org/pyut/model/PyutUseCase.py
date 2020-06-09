
from org.pyut.model.PyutLinkedObject import PyutLinkedObject


class PyutUseCase(PyutLinkedObject):

    DEFAULT_USE_CASE_NAME: str = 'UseCase'
    """
    """
    def __init__(self, name: str = DEFAULT_USE_CASE_NAME):
        super().__init__(name)
