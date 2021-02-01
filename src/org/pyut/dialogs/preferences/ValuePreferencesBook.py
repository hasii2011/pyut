
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import BK_DEFAULT

from wx import ID_ANY
from wx import StaticBox

from wx import Bitmap
from wx import BoxSizer
from wx import ImageList
from wx import Panel
from wx import StaticBoxSizer
from wx import Toolbook
from wx import VERTICAL
from wx import Window

from wx.lib.embeddedimage import PyEmbeddedImage

from org.pyut.dialogs.preferences.NoteAttributesContainer import NoteAttributesContainer
from org.pyut.dialogs.preferences.TextAttributesContainer import TextAttributesContainer
from org.pyut.preferences.Dimensions import Dimensions

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.dialogs.preferences.DirectionEnum import DirectionEnum
from org.pyut.dialogs.preferences.TextContainer import TextContainer
from org.pyut.dialogs.preferences.DimensionsContainer import DimensionsContainer

from org.pyut.resources.img.DefaultPreferences import embeddedImage as DefaultPreferences

from org.pyut.resources.img.toolbar.embedded16.ImgToolboxNote import embeddedImage as ImgToolboxNote
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxText import embeddedImage as ImgToolboxText
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxClass import embeddedImage as ImgToolboxClass

from org.pyut.general.Globals import _


def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0


class ValuePreferencesBook(Toolbook):

    VERTICAL_GAP:   int = 2
    HORIZONTAL_GAP: int = 5

    def __init__(self, parent: Window, wxId: int):

        super().__init__(parent, wxId, style=BK_DEFAULT)

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        #
        # Controls we are going to create
        #
        self._classNameContainer: TextContainer       = cast(TextContainer, None)
        self._classDimensionsContainer:    DimensionsContainer = cast(DimensionsContainer, None)

        self._interfaceNameContainer: TextContainer = cast(TextContainer, None)
        self._useCaseNameContainer:   TextContainer = cast(TextContainer, None)
        self._actorNameContainer:     TextContainer = cast(TextContainer, None)
        self._methodNameContainer:    TextContainer = cast(TextContainer, None)

        self._createControls()
        self._setControlValues()

        self._valueChanged: bool = False

    def updatePreferences(self) -> bool:
        """
        Called by main dialog to ask it to update any changed preferences

        Returns: `True` if any values were updated else it returns `False`
        """
        return self._valueChanged

    def _createControls(self):

        embeddedImages: List[PyEmbeddedImage] = [ImgToolboxNote, ImgToolboxText, ImgToolboxClass, DefaultPreferences]
        imageList:      ImageList             = ImageList(width=16, height=16)

        for embeddedImage in embeddedImages:
            bmp: Bitmap = embeddedImage.GetBitmap()
            imageList.Add(bmp)

        self.AssignImageList(imageList)

        imageIdGenerator = getNextImageID(imageList.GetImageCount())

        notePanel:         NoteAttributesContainer = NoteAttributesContainer(parent=self)
        textPanel:         TextAttributesContainer = TextAttributesContainer(parent=self)
        classPanel:        Panel = self.__createClassControls()
        defaultNamesPanel: Panel = self.__createDefaultNameControls()

        self.AddPage(notePanel,         text='Notes', select=True, imageId=next(imageIdGenerator))
        self.AddPage(textPanel,         text='Text',  select=False, imageId=next(imageIdGenerator))
        self.AddPage(classPanel,        text='Class', select=False, imageId=next(imageIdGenerator))
        self.AddPage(defaultNamesPanel, text='Names', select=False, imageId=next(imageIdGenerator))

    def _bindControls(self):

        pass
        # self.Bind(EVT_CHECKBOX, self._onTextBoldValueChanged,      id=self._cbBoldTextId)
        # self.Bind(EVT_CHECKBOX, self._onTextItalicizeValueChanged, id=self._cbItalicizeTextId)
        #
        # self.Bind(EVT_COMBOBOX, self._onFontSelectionChanged, id=self._cbxFontSelectionId)

    def _setControlValues(self):
        """
        Set the default values on the controls.
        """
        # self._noteTextContainer.textValue  = self._preferences.noteText
        # self._noteDimensions.dimensions    = self._preferences.noteDimensions

        self._classNameContainer.textValue        = self._preferences.className
        self._classDimensionsContainer.dimensions = self._preferences.classDimensions

    def __createClassControls(self) -> Panel:

        p:        Panel    = Panel(self, ID_ANY)
        szrClass: BoxSizer = BoxSizer(VERTICAL)

        classNameContainer:       TextContainer       = TextContainer(parent=p, labelText=_('Default Name'), valueChangedCallback=self.__classNameChanged)
        classDimensionsContainer: DimensionsContainer = DimensionsContainer(parent=p, displayText=_('Class Width/Height'), valueChangedCallback=self.__classDimensionsChanged)

        szrClass.Add(classNameContainer, 0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrClass.Add(classDimensionsContainer,   0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)

        self._classNameContainer       = classNameContainer
        self._classDimensionsContainer = classDimensionsContainer

        p.SetSizer(szrClass)
        p.Fit()

        return p

    def __createDefaultNameControls(self) -> Panel:

        p: Panel = Panel(self, ID_ANY)
        # szrNames: StaticBoxSizer = self.__createStaticBoxSizer(_('Default Names'), direction=VERTICAL)
        szrNames: BoxSizer = BoxSizer(VERTICAL)

        interfaceNameContainer: TextContainer = TextContainer(parent=p, labelText=_('Interface Name'), valueChangedCallback=self.__interfaceNameChanged)
        useCaseNameContainer:   TextContainer = TextContainer(parent=p, labelText=_('Use Case Name'),  valueChangedCallback=self.__useCaseNameChanged)
        actorNameContainer:     TextContainer = TextContainer(parent=p, labelText=_('Actor Name'),     valueChangedCallback=self.__actorNameChanged)
        methodNameContainer:    TextContainer = TextContainer(parent=p, labelText=_('Method Name'),    valueChangedCallback=self.__methodNameChanged)

        szrNames.Add(interfaceNameContainer, 0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrNames.Add(useCaseNameContainer,   0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrNames.Add(actorNameContainer,     0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrNames.Add(methodNameContainer,    0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)

        self._interfaceNameContainer: TextContainer = interfaceNameContainer
        self._useCaseNameContainer:   TextContainer = useCaseNameContainer
        self._actorNameContainer:     TextContainer = actorNameContainer
        self._methodNameContainer:    TextContainer = methodNameContainer

        p.SetSizer(szrNames)
        p.Fit()

        return p

    def __createStaticBoxSizer(self, displayText: str, direction: DirectionEnum) -> StaticBoxSizer:

        box:       StaticBox      = StaticBox(self, ID_ANY, displayText)
        sBoxSizer: StaticBoxSizer = StaticBoxSizer(box, direction.value)

        return sBoxSizer

    def __classNameChanged(self, newValue: str):
        self._preferences.className = newValue

    def __classDimensionsChanged(self, newValue: Dimensions):
        self._preferences.classDimensions = newValue

    def __interfaceNameChanged(self, newValue: str):
        pass

    def __useCaseNameChanged(self, newValue: str):
        pass

    def __actorNameChanged(self, newValue: str):
        pass

    def __methodNameChanged(self, newValue: str):
        pass
