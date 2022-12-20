
from typing import List

from wx import BK_DEFAULT

from wx import Bitmap
from wx import ID_ANY
from wx import ImageList
from wx import Toolbook

from wx.lib.embeddedimage import PyEmbeddedImage

from pyut.dialogs.preferences.valuecontainers.ClassControl import ClassControl

from pyut.dialogs.preferences.valuecontainers.DefaultNamesControl import DefaultNamesControl

from pyut.dialogs.preferences.valuecontainers.NoteAttributesControl import NoteAttributesControl
from pyut.dialogs.preferences.valuecontainers.TextAttributesContainer import TextAttributesContainer

from pyut.resources.img.DefaultPreferences import embeddedImage as DefaultPreferences

from pyut.resources.img.toolbar.embedded16.ImgToolboxNote import embeddedImage as ImgToolboxNote
from pyut.resources.img.toolbar.embedded16.ImgToolboxText import embeddedImage as ImgToolboxText
from pyut.resources.img.toolbar.embedded16.ImgToolboxClass import embeddedImage as ImgToolboxClass


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

    def __init__(self, parent):

        super().__init__(parent, ID_ANY, style=BK_DEFAULT)

        self._createControls()

    def _createControls(self):

        embeddedImages: List[PyEmbeddedImage] = [ImgToolboxNote, ImgToolboxText, ImgToolboxClass, DefaultPreferences]
        imageList:      ImageList             = ImageList(width=16, height=16)

        for embeddedImage in embeddedImages:
            bmp: Bitmap = embeddedImage.GetBitmap()
            imageList.Add(bmp)

        self.AssignImageList(imageList)

        imageIdGenerator = getNextImageID(imageList.GetImageCount())

        notePanel:  NoteAttributesControl   = NoteAttributesControl(parent=self)
        textPanel:  TextAttributesContainer = TextAttributesContainer(parent=self)
        classPanel: ClassControl            = ClassControl(parent=self)

        defaultNamesPanel: DefaultNamesControl      = DefaultNamesControl(parent=self)

        self.AddPage(notePanel,         text='Notes', select=True,  imageId=next(imageIdGenerator))
        self.AddPage(textPanel,         text='Text',  select=False, imageId=next(imageIdGenerator))
        self.AddPage(classPanel,        text='Class', select=False, imageId=next(imageIdGenerator))
        self.AddPage(defaultNamesPanel, text='Names', select=False, imageId=next(imageIdGenerator))
