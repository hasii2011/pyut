
from org.pyut.errorcontroller.IErrorView import IErrorView
from org.pyut.errorcontroller.PyutException import PyutException


class RaiseErrorView(IErrorView):
    """
    This class is an error view which will raise all errors as exceptions

    To use it, use the mediator methods:
    ```python
      mediator: Mediator = Mediator()
      ...
      errorManager = mediator.getErrorManager()
      errorManager.changeType(ErrorViewTypes.RAISE_ERROR_VIEW)

      errorManager.newFatalError("This is a message", "...")
      errorManager.newWarning("This is a message", "...")
      errorManager.newInformation("This is a message", "...")

    ```

    """

    def newFatalError(self, msg, title=None, parent=None):
        raise PyutException(f"FATAL ERROR: {title} - {msg}")

    def newWarning(self, msg, title=None, parent=None):
        raise PyutException(f"WARNING: {title} - {msg}")

    def displayInformation(self, msg, title=None, parent=None):
        raise PyutException(f"INFORMATION: {title} 0 {msg}")
