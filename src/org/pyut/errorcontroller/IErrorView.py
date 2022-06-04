from wx import Frame


class IErrorView:
    """
    Prototypical abstract class
    """
    def newFatalError(self, msg: str, title: str = None, parent: Frame = None):
        pass

    def newWarning(self, msg: str, title: str = None, parent: Frame = None):
        pass

    def newInformation(self, msg: str, title: str = None, parent: Frame = None):
        pass

    def displayInformation(self, msg: str, title: str = None, parent: Frame = None):
        pass
