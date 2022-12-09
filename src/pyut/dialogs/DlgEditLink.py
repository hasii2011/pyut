
from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_CENTRE
from wx import ALIGN_LEFT
from wx import ALIGN_RIGHT
from wx import ALL
from wx import CANCEL
from wx import CAPTION
from wx import CLOSE_BOX
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import GROW
from wx import ID_ANY
from wx import ID_OK
from wx import ID_CANCEL
from wx import OK
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import Sizer
from wx import StaticBitmap
from wx import VERTICAL

from wx import BoxSizer
from wx import CommandEvent
from wx import Dialog
from wx import FlexGridSizer
from wx import Size
from wx import StaticText
from wx import TextCtrl

from wx.lib.embeddedimage import PyEmbeddedImage

from pyut.PyutUtils import PyutUtils

from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType


[
    TXT_CARDINALITY_A,
    TXT_CARDINALITY_B,
    TXT_RELATIONSHIP,
] = PyutUtils.assignID(3)


class DlgEditLink (Dialog):
    """
    Dialog for the link (between classes) editing.

    to use it :
        with DlgEditLink(None, ID_ANY, diagramShape.pyutObject) as dlg:
            dlg.ShowModal()

    The input PyutLink is only updated on Ok;  Else if the dialogs is
    "canceled" any updated values are discarded

    """
    def __init__(self, parent, pyutLink: PyutLink):
        """
        """
        super().__init__(parent, ID_ANY, "Edit Link", style=RESIZE_BORDER | CAPTION | CLOSE_BOX | STAY_ON_TOP)

        self.logger: Logger = getLogger(__name__)

        self._pyutLink:     PyutLink = pyutLink
        self._relationship: str = self._pyutLink.name
        self._cardinalityA: str = self._pyutLink.sourceCardinality
        self._cardinalityB: str = self._pyutLink.destinationCardinality

        #  labels
        lblCardA: StaticText = StaticText(self, ID_ANY, "Cardinality",  style=ALIGN_LEFT)
        lblRela:  StaticText = StaticText(self, ID_ANY, "Relationship", style=ALIGN_CENTRE)
        lblCardB: StaticText = StaticText(self, ID_ANY, "Cardinality",  style=ALIGN_RIGHT)

        self._imgArrow: StaticBitmap = self._linkImage(pyutLink.linkType)

        #  text
        self._txtCardinalityA: TextCtrl = TextCtrl(self, TXT_CARDINALITY_A, "", size=Size(50, 20))
        self._txtRelationship: TextCtrl = TextCtrl(self, TXT_RELATIONSHIP,  "", size=Size(100, 20))
        self._txtCardinalityB: TextCtrl = TextCtrl(self, TXT_CARDINALITY_B, "", size=Size(50, 20))

        szr1: FlexGridSizer = FlexGridSizer(cols=3, rows=4, hgap=30, vgap=5)
        szr1.AddMany([
            (self._imgArrow, 0, ALIGN_LEFT), (50,10), (50,10),
            (lblCardA, 0, ALIGN_LEFT), (lblRela,  0, ALIGN_CENTER_HORIZONTAL), (lblCardB, 0, ALIGN_RIGHT),
            (self._txtCardinalityA, 0, ALIGN_LEFT),
            (self._txtRelationship, 0, ALIGN_CENTER_HORIZONTAL),
            (self._txtCardinalityB, 0, ALIGN_RIGHT)])
        szr1.AddGrowableCol(0)
        szr1.AddGrowableCol(1)
        szr1.AddGrowableCol(2)

        buttonContainer: Sizer = self.CreateStdDialogButtonSizer(OK | CANCEL)
        # btnOk.SetDefault()

        # mainSizer :
        #        szr1
        #        buttonContainer
        mainSizer: BoxSizer = BoxSizer(VERTICAL)
        mainSizer.Add(szr1, 0, GROW | ALL, 10)
        mainSizer.Add(buttonContainer, 0, ALIGN_RIGHT | ALL, 10)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)

        self._setValues(self._relationship, self._cardinalityA, self._cardinalityB)

        #  text events
        self.Bind(EVT_TEXT, self._onTxtCardinalityAChange, id=TXT_CARDINALITY_A)
        self.Bind(EVT_TEXT, self._onTxtCardinalityBChange, id=TXT_CARDINALITY_B)
        self.Bind(EVT_TEXT, self._onTxtRelationshipChange, id=TXT_RELATIONSHIP)
        #  button events
        self.Bind(EVT_BUTTON, self._onCmdOk,     id=ID_OK)
        self.Bind(EVT_BUTTON, self._onCmdCancel, id=ID_CANCEL)

        mainSizer.Fit(self)

    def _createDialogButtonsContainer(self, buttons=OK) -> Sizer:

        hs: Sizer = self.CreateSeparatedButtonSizer(buttons)
        return hs

    def _linkImage(self, linkType: PyutLinkType) -> StaticBitmap:
        """
        Provide an example image in linkImage
        """
        from pyut.resources.img.toolbar.embedded16.ImgToolboxRelationshipAssociation import embeddedImage as ImgToolboxRelationshipAssociation
        from pyut.resources.img.toolbar.embedded16.ImgToolboxRelationshipAggregation import embeddedImage as ImgToolboxRelationshipAggregation
        from pyut.resources.img.toolbar.embedded16.ImgToolboxRelationshipComposition import embeddedImage as ImgToolboxRelationshipComposition
        linkTypeToImage = {
            PyutLinkType.ASSOCIATION: ImgToolboxRelationshipAssociation,
            PyutLinkType.AGGREGATION: ImgToolboxRelationshipAggregation,
            PyutLinkType.COMPOSITION: ImgToolboxRelationshipComposition,
        }
        embeddedImage: PyEmbeddedImage = linkTypeToImage[linkType]
        linkImage:     StaticBitmap    = StaticBitmap(self, ID_ANY, embeddedImage.GetBitmap())

        return linkImage

    def _onTxtCardinalityAChange(self, event):
        """
        Event occurring when TXT_CARDINALITY_A change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._cardinalityA = event.GetString()

    def _onTxtCardinalityBChange(self, event):
        """
        Event occurring when TXT_CARDINALITY_B change
        """
        self._cardinalityB = event.GetString()

    def _onTxtRelationshipChange(self, event):
        """
        Event occurring when TXT_RELATIONSHIP change
        """
        self._relationship = event.GetString()

    # noinspection PyUnusedLocal
    def _onCmdOk(self, event: CommandEvent):
        """
        Handle click on "Ok" button

        Args:
            event:
        """
        self._pyutLink.name = self._relationship

        self._pyutLink.sourceCardinality      = self._cardinalityA
        self._pyutLink.destinationCardinality = self._cardinalityB

        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event: CommandEvent):
        """
        """
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)

    def _setValues(self, relationship: str, cardinalityA: str, cardinalityB: str):
        """

        Args:
            relationship: the relationship between the two entities
            cardinalityA: the source cardinality
            cardinalityB: the source cardinality
        """
        self._txtRelationship.SetValue(relationship)

        self._txtCardinalityA.SetValue(cardinalityA)
        self._txtCardinalityB.SetValue(cardinalityB)
