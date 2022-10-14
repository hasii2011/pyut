
from abc import ABCMeta
from abc import abstractmethod

from wx import Frame
from wx import ID_ANY
from wx import SplitterWindow

from org.pyut.uiv2.IPyutProject import IPyutProject


class MyMeta(ABCMeta, type(SplitterWindow)):        # type: ignore
    """
    I have know idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class IPyutUI(SplitterWindow, metaclass=MyMeta):

    def __init__(self, topLevelWindow: Frame):
        super().__init__(parent=topLevelWindow, id=ID_ANY)

    # @abstractmethod
    # def openFile(self, filename, project: IPyutProject = None) -> bool:
    #     pass
