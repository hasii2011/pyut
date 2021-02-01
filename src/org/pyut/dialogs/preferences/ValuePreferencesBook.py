
from typing import List

from logging import Logger
from logging import getLogger

from wx import BK_DEFAULT


from wx import Bitmap
from wx import ImageList
from wx import Toolbook
from wx import Window

from wx.lib.embeddedimage import PyEmbeddedImage

from org.pyut.dialogs.preferences.valuecontainers.ClassContainer import ClassContainer
from org.pyut.dialogs.preferences.valuecontainers.DefaultNamesContainer import DefaultNamesContainer
from org.pyut.dialogs.preferences.valuecontainers.NoteAttributesContainer import NoteAttributesContainer
from org.pyut.dialogs.preferences.valuecontainers.TextAttributesContainer import TextAttributesContainer

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.resources.img.DefaultPreferences import embeddedImage as DefaultPreferences

from org.pyut.resources.img.toolbar.embedded16.ImgToolboxNote import embeddedImage as ImgToolboxNote
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxText import embeddedImage as ImgToolboxText
from org.pyut.resources.img.toolbar.embedded16.ImgToolboxClass import embeddedImage as ImgToolboxClass


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

        self._createControls()

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
        classPanel:        ClassContainer          = ClassContainer(parent=self)
        defaultNamesPanel: DefaultNamesContainer   = DefaultNamesContainer(parent=self)

        self.AddPage(notePanel,         text='Notes', select=True,  imageId=next(imageIdGenerator))
        self.AddPage(textPanel,         text='Text',  select=False, imageId=next(imageIdGenerator))
        self.AddPage(classPanel,        text='Class', select=False, imageId=next(imageIdGenerator))
        self.AddPage(defaultNamesPanel, text='Names', select=False, imageId=next(imageIdGenerator))
