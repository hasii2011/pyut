
from org.pyut.errorcontroller.AbstractErrorView import AbstractErrorView


class RaiseErrorView(AbstractErrorView):
    """
    This class is an error view which will raise all errors as
    text message box.

    To use it, use the mediator methods :
     - mediator = Mediator.getMediator()
     - ...
     - errorManager = mediator.getErrorManager()
     - errorManager.changeType(ErrorViewTypes.RAISE_ERROR_VIEW)
     -
     - errorManager.newFatalError("This is a message", "...")
     - errorManager.newWarning("This is a message", "...")
     - errorManager.newInformation("This is a message", "...")
     - ...

    @author C.Dutoit
    """

    def newFatalError(self, msg, title=None, parent=None):
        raise Exception(f"FATAL ERROR: {title} - {msg}")

    def newWarning(self, msg, title=None, parent=None):
        raise Exception(f"WARNING: {title} - {msg}")

    def displayInformation(self, msg, title=None, parent=None):
        raise Exception(f"INFORMATION: {title} 0 {msg}")

