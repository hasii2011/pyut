from wx import CANCEL
from wx import CENTER
from wx import OK

from wx import TextEntryDialog
from wx import Window


class DlgEditUseCase(TextEntryDialog):
    """
    Syntactic sugar around a text entry dialog specifically for
    editing a use case name
    Usage:

        with DlgEditUseCase(umlFrame, useCaseName=pyutUseCase.name) as dlg:
            if dlg.ShowModal() == ID_OK:
                pyutUseCase.name = dlg.GetValue()
    """
    def __init__(self, parent: Window, useCaseName: str):
        super().__init__(parent, message="Use Case Name", caption="Edit Use Case Name", value=useCaseName, style=OK | CANCEL | CENTER)


class DlgEditActor(TextEntryDialog):
    """
    Syntactic sugar around a text entry dialog specifically for
    editing an actor's name
    Usage:

        with DlgEditActor(umlFrame, useCaseName=pyutActor.name) as dlg:
            if dlg.ShowModal() == ID_OK:
                pyutActor.name = dlg.GetValue()
    """
    def __init__(self, parent: Window, actorName: str):
        super().__init__(parent, message="Actor Name", caption="Edit Actor Name", value=actorName, style=OK | CANCEL | CENTER)


class DlgEditDiagramTitle(TextEntryDialog):
    """
    Syntactic sugar around a text entry dialog specifically for
    editing a diagram's name
    Usage:

        with DlgEditDiagramTitle(umlFrame, diagramTitle=diagram.title) as dlg:
            if dlg.ShowModal() == ID_OK:
                diagram.title = dlg.GetValue()
    """
    def __init__(self, parent: Window, diagramTitle: str):
        super().__init__(parent, message='Diagram Title', caption='Edit Diagram Title', value=diagramTitle, style=OK | CANCEL | CENTER)
