
from wx import DefaultPosition

from wx import LC_REPORT

from wx.lib.agw import ultimatelistctrl as ULC
from wx.lib.agw.ultimatelistctrl import ULC_REPORT
from wx.lib.agw.ultimatelistctrl import ULC_SORT_ASCENDING
from wx.lib.agw.ultimatelistctrl import ULC_VRULES

from wx.lib.mixins.listctrl import ListRowHighlighter


class DebugListControl(ULC.UltimateListCtrl, ListRowHighlighter):
    def __init__(self, parent, ID, pos=DefaultPosition, size=(600, 200), agwStyle=ULC_REPORT | ULC_SORT_ASCENDING | ULC_VRULES, style=LC_REPORT):

        ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle=agwStyle, style=style)
        ListRowHighlighter.__init__(self)

