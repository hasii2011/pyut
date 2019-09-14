#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

#from wxPython.wx import *
#import wx
from AppFrame import *
from DlgEditClass2 import *
from DlgEditLink import *
from DlgHelp import *
from IoFile import *
from PluginManager import *
from PyutApp import *
from PyutClass import *
from PyutField import *
from PyutFileDropTarget import *
from PyutLink import *
from PyutMethod import *
from PyutModifier import *
from PyutObject import *
from PyutParam import *
from PyutPrintout import *
from PyutStereotype import PyutStereotype
from PyutType import PyutType
from PyutVisibility import PyutVisibility
from PyutXml import *
from UmlFrame import *
from dlgEditMethod import *
from mediator import *
from singleton import *
from FlyweightString import *
from PyutLinkedObject import *
from PyutNote import *
from PyutActor import *
from PyutUseCase import *

# OGL

from OglObject import *
from OglClass import *
from OglNote import *
from OglActor import *
from OglLink import *
from OglNoteLink import *
from OglAssociation import *
from OglAggregation import *
from OglComposition import *
from OglInheritance import *
from OglInterface import *
from OglLinkFactory import *

display = [
    "PyutClass",
    "PyutField",
    "PyutLink",
    "PyutLinkedObject",
    "PyutNote",
    "PyutUseCase",
    "PyutActor",
    "PyutMethod",
    "PyutModifier",
    "PyutObject",
    "PyutParam",
    "PyutStereotype",
    "PyutType",
    "PyutVisibility",
    "Mediator",
    "Singleton",
    "FlyweightString",
    "object"
]

displayOgl = [
    "OglObject",
    "OglClass",
    "OglNote",
    "OglActor",
    "OglLink",
    "OglNoteLink",
    "OglAssociation",
    "OglAggregation",
    "OglComposition",
    "OglInheritance",
    "OglInterface",
    "OglLinkFactory"
]

