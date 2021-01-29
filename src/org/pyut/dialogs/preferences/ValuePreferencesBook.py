
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import BK_DEFAULT
from wx import CB_READONLY
from wx import CheckBox
from wx import ComboBox
from wx import CommandEvent
from wx import EVT_CHECKBOX
from wx import EVT_COMBOBOX
from wx import HORIZONTAL
from wx import ID_ANY
from wx import RadioButton
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

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.preferences.DirectionEnum import DirectionEnum
from org.pyut.dialogs.preferences.TextContainer import TextContainer
from org.pyut.dialogs.preferences.TextFontEnum import TextFontEnum
from org.pyut.dialogs.preferences.WidthHeightContainer import WidthHeightContainer
from org.pyut.preferences.PyutPreferences import PyutPreferences

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
        self._noteTextContainer:   TextContainer        = cast(TextContainer, None)
        self._noteWidthHeight:     WidthHeightContainer = cast(WidthHeightContainer, None)

        # Declare controls we need access to and will be created by the createXXXControls methods
        [self._cbBoldTextId, self._cbItalicizeTextId, self._cbxFontSelectionId] = PyutUtils.assignID(3)

        self._textWidthHeight:  WidthHeightContainer = cast(WidthHeightContainer, None)
        self._cbBoldText:       RadioButton   = cast(RadioButton, None)
        self._cbItalicizeText:  RadioButton   = cast(RadioButton, None)
        self._cbxFontSelection: ComboBox      = cast(ComboBox, None)

        self._classNameContainer:  TextContainer        = cast(TextContainer, None)
        self._classWidthHeight:    WidthHeightContainer = cast(WidthHeightContainer, None)

        self._interfaceNameContainer: TextContainer = cast(TextContainer, None)
        self._useCaseNameContainer:   TextContainer = cast(TextContainer, None)
        self._actorNameContainer:     TextContainer = cast(TextContainer, None)
        self._methodNameContainer:    TextContainer = cast(TextContainer, None)

        self._createControls()
        self._BindControls()
        self._setControlValues()

        self._valueChanged: bool = False

    def updatePreferences(self) -> bool:
        """
        Called by main dialog to ask it to update any changed preferences

        Returns: `True` if any values were updated else it returns `False`
        """
        if self._noteTextContainer.valueChanged is True:
            self._valueChanged = True
            self._preferences.noteText       = self._noteTextContainer.textValue

        return self._valueChanged

    def _createControls(self):

        embeddedImages: List[PyEmbeddedImage] = [ImgToolboxNote, ImgToolboxText, ImgToolboxClass, DefaultPreferences]
        imageList:      ImageList             = ImageList(width=16, height=16)

        for embeddedImage in embeddedImages:
            bmp: Bitmap = embeddedImage.GetBitmap()
            imageList.Add(bmp)

        self.AssignImageList(imageList)

        imageIdGenerator = getNextImageID(imageList.GetImageCount())

        notePanel:         Panel = self.__createNoteControls()
        textPanel:         Panel = self.__createTextControls()
        classPanel:        Panel = self.__createClassControls()
        defaultNamesPanel: Panel = self.__createDefaultNameControls()

        self.AddPage(notePanel,         text='Notes', select=True, imageId=next(imageIdGenerator))
        self.AddPage(textPanel,         text='Text',  select=False, imageId=next(imageIdGenerator))
        self.AddPage(classPanel,        text='Class', select=False, imageId=next(imageIdGenerator))
        self.AddPage(defaultNamesPanel, text='Names', select=False, imageId=next(imageIdGenerator))

    def _BindControls(self):

        self.Bind(EVT_CHECKBOX, self._onTextBoldValueChanged,      id=self._cbBoldTextId)
        self.Bind(EVT_CHECKBOX, self._onTextItalicizeValueChanged, id=self._cbItalicizeTextId)

        self.Bind(EVT_COMBOBOX, self._onFontSelectionChanged, id=self._cbxFontSelectionId)

    def _setControlValues(self):
        """
        Set the default values on the controls.
        """
        self._noteTextContainer.textValue = self._preferences.noteText
        self._noteWidthHeight.widthValue  = self._preferences.noteDimensions.width
        self._noteWidthHeight.heightValue = self._preferences.noteDimensions.height
        self._textWidthHeight.widthValue  = self._preferences.textDimensions.width
        self._textWidthHeight.heightValue = self._preferences.textDimensions.height

    def _onTextBoldValueChanged(self, event: CommandEvent):

        val: bool = event.IsChecked()

        self._valueChanged = True
        self.logger.warning(f'bold text new value: `{val}`')

    def _onTextItalicizeValueChanged(self, event: CommandEvent):

        val: bool = event.IsChecked()
        self._valueChanged = True
        self.logger.warning(f'italicize text new value: `{val}`')

    def _onFontSelectionChanged(self, event: CommandEvent):

        newFontName: str = event.GetString()
        self._valueChanged = True
        self.logger.warning(f'Font name change: `{newFontName}`')

        event.Skip(True)

    def __createNoteControls(self) -> Panel:

        p:        Panel    = Panel(self, ID_ANY)
        szrNotes: BoxSizer = BoxSizer(VERTICAL)

        szrDefaultNoteText: BoxSizer             = self.__createDefaultNoteTextContainer(parent=p)
        szrNoteSize:        WidthHeightContainer = self.__createDefaultNoteSizeContainer(parent=p)

        szrNotes.Add(szrDefaultNoteText, 0, ALL, ValuePreferencesBook.VERTICAL_GAP)
        szrNotes.Add(szrNoteSize,        0, ALL, ValuePreferencesBook.VERTICAL_GAP)

        p.SetSizer(szrNotes)
        p.Fit()

        return p

    def __createDefaultNoteTextContainer(self, parent: Window) -> TextContainer:

        noteTextContainer: TextContainer = TextContainer(parent=parent, labelText=_('Default Note Text'))

        self._noteTextContainer = noteTextContainer

        return noteTextContainer

    def __createDefaultNoteSizeContainer(self, parent: Window) -> WidthHeightContainer:

        noteWidthHeight:  WidthHeightContainer = WidthHeightContainer(parent=parent, displayText=_('Note Width/Height'), minValue=100, maxValue=300)

        self._noteWidthHeight = noteWidthHeight

        return noteWidthHeight

    def __createTextControls(self) -> Panel:

        p: Panel = Panel(self, ID_ANY)
        # szrText: StaticBoxSizer = self.__createStaticBoxSizer(_('Text'), direction=VERTICAL)
        szrText: BoxSizer = BoxSizer(VERTICAL)

        self._textWidthHeight: WidthHeightContainer = WidthHeightContainer(parent=p, displayText=_('Text Width/Height'), minValue=100, maxValue=300)

        szrText.Add(self._textWidthHeight,                     0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrText.Add(self.__createTextStyleContainer(parent=p), 0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrText.Add(self.__createTextFontSelector(parent=p),   0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)

        p.SetSizer(szrText)
        p.Fit()

        return p

    def __createTextStyleContainer(self, parent: Window) -> BoxSizer:

        styleContainer: BoxSizer = BoxSizer(HORIZONTAL)

        self._cbBoldText:      CheckBox = CheckBox(parent=parent, id=self._cbBoldTextId, label=_('Bold Text'))
        self._cbItalicizeText: CheckBox = CheckBox(parent=parent, id=self._cbItalicizeTextId, label=_('Italicize Text'))

        styleContainer.Add(self._cbBoldText, 0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        styleContainer.Add(self._cbItalicizeText, 0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)

        return styleContainer

    def __createTextFontSelector(self, parent: Window) -> ComboBox:

        fontChoices = []
        for fontName in TextFontEnum:
            fontChoices.append(fontName.value)

        self._cbxFontSelection: ComboBox = ComboBox(parent, self._cbxFontSelectionId, choices=fontChoices, style=CB_READONLY)

        return self._cbxFontSelection

    def __createClassControls(self) -> Panel:

        p: Panel = Panel(self, ID_ANY)
        # szrClass: StaticBoxSizer = self.__createStaticBoxSizer(_('Class'), direction=VERTICAL)
        szrClass: BoxSizer = BoxSizer(VERTICAL)

        classNameContainer: TextContainer        = TextContainer(parent=p, labelText=_('Default Name'))
        classWidthHeight:   WidthHeightContainer = WidthHeightContainer(parent=p, displayText=_('Class Width/Height'), minValue=100, maxValue=300)

        szrClass.Add(classNameContainer, 0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)
        szrClass.Add(classWidthHeight,   0, ALL, ValuePreferencesBook.HORIZONTAL_GAP)

        self._classWidthHeight = szrClass

        p.SetSizer(szrClass)
        p.Fit()

        return p

    def __createDefaultNameControls(self) -> Panel:

        p: Panel = Panel(self, ID_ANY)
        # szrNames: StaticBoxSizer = self.__createStaticBoxSizer(_('Default Names'), direction=VERTICAL)
        szrNames: BoxSizer = BoxSizer(VERTICAL)

        interfaceNameContainer: TextContainer = TextContainer(parent=p, labelText=_('Interface Name'))
        useCaseNameContainer:   TextContainer = TextContainer(parent=p, labelText=_('Use Case Name'))
        actorNameContainer:     TextContainer = TextContainer(parent=p, labelText=_('Actor Name'))
        methodNameContainer:    TextContainer = TextContainer(parent=p, labelText=_('Method Name'))

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
