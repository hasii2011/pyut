#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "$Revision: 1.38 $"
__author__  = "EI5, eivd, Group Burgbacher - Waelti"
__date__    = "2001-12-12"

from pyutUtils       import *
from singleton       import Singleton
from PyutConsts      import *
from PyutMethod      import *
from PyutClass       import *
from PyutPreferences import *
from MiniOgl         import *
from ToolboxOwner    import *

# Dialogs
from DlgEditClass2   import *
from DlgEditNote     import *
from DlgEditUseCase  import *
from DlgEditLink     import *

from pyutVersion import getPyUtVersion
__PyUtVersion__ = getPyUtVersion()

# an enum of the supported actions
[
    ACTION_SELECTOR,
    ACTION_NEW_CLASS,
    ACTION_NEW_ACTOR,
    ACTION_NEW_USECASE,
    ACTION_NEW_NOTE,
    ACTION_NEW_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK,
    ACTION_DEST_IMPLEMENT_LINK,
    ACTION_DEST_INHERIT_LINK,
    ACTION_DEST_AGGREGATION_LINK,
    ACTION_DEST_COMPOSITION_LINK,
    ACTION_DEST_ASSOCIATION_LINK,
    ACTION_DEST_NOTE_LINK,
    ACTION_NEW_SD_INSTANCE,
    ACTION_NEW_SD_MESSAGE,
    ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN,  # Patch from D.Dabrowsky, 20060129
    ACTION_ZOOM_OUT # Patch from D.Dabrowsky, 20060129
] = range(22)

# a table of the next action to select
NEXT_ACTION = {
    ACTION_SELECTOR              : ACTION_SELECTOR,
    ACTION_NEW_CLASS             : ACTION_SELECTOR,
    ACTION_NEW_NOTE              : ACTION_SELECTOR,
    ACTION_NEW_IMPLEMENT_LINK    : ACTION_DEST_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK      : ACTION_DEST_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK  : ACTION_DEST_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK  : ACTION_DEST_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK  : ACTION_DEST_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK         : ACTION_DEST_NOTE_LINK,
    ACTION_DEST_IMPLEMENT_LINK   : ACTION_SELECTOR,
    ACTION_DEST_INHERIT_LINK     : ACTION_SELECTOR,
    ACTION_DEST_AGGREGATION_LINK : ACTION_SELECTOR,
    ACTION_DEST_COMPOSITION_LINK : ACTION_SELECTOR,
    ACTION_DEST_ASSOCIATION_LINK : ACTION_SELECTOR,
    ACTION_DEST_NOTE_LINK        : ACTION_SELECTOR,
    ACTION_NEW_ACTOR             : ACTION_SELECTOR,
    ACTION_NEW_USECASE           : ACTION_SELECTOR,

    ACTION_NEW_SD_INSTANCE       : ACTION_SELECTOR,
    ACTION_NEW_SD_MESSAGE        : ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN               : ACTION_ZOOM_IN,  # Patch from D.Dabrowsky, 20060129
    ACTION_ZOOM_IN               : ACTION_ZOOM_OUT, # Patch from D.Dabrowsky, 20060129
}

# list of actions which are source events
SOURCE_ACTIONS = [
    ACTION_NEW_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK,
    ACTION_NEW_SD_MESSAGE,

]
# list of actions which are destination events
DEST_ACTIONS = [
    ACTION_DEST_IMPLEMENT_LINK,
    ACTION_DEST_INHERIT_LINK,
    ACTION_DEST_AGGREGATION_LINK,
    ACTION_DEST_COMPOSITION_LINK,
    ACTION_DEST_ASSOCIATION_LINK,
    ACTION_DEST_NOTE_LINK,
    ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN, # Patch from D.Dabrowsky, 20060129
    ACTION_ZOOM_OUT # Patch from D.Dabrowsky, 20060129
]

# OglLink constants according to the current action
LINK_TYPE = {
    ACTION_DEST_IMPLEMENT_LINK   : OGL_INTERFACE,
    ACTION_DEST_INHERIT_LINK     : OGL_INHERITANCE,
    ACTION_DEST_AGGREGATION_LINK : OGL_AGGREGATION,
    ACTION_DEST_COMPOSITION_LINK : OGL_COMPOSITION,
    ACTION_DEST_ASSOCIATION_LINK : OGL_ASSOCIATION,
    ACTION_DEST_NOTE_LINK        : OGL_NOTELINK,
    ACTION_DEST_SD_MESSAGE       : OGL_SD_MESSAGE,
}

# messages for the status bar
a = _("Click on the source class")
b = _("Now, click on the destination class")

MESSAGES = {
    ACTION_SELECTOR              : _("Ready"),
    ACTION_NEW_CLASS             : _("Click where you want to put "
                                     "the new class"),
    ACTION_NEW_NOTE              : _("Click where you want to put "
                                     "the new note"),
    ACTION_NEW_ACTOR             : _("Click where you want to put "
                                     "the new actor"),
    ACTION_NEW_USECASE           : _("Click where you want to put "
                                     "the new use case"),
    ACTION_NEW_SD_INSTANCE       : _("Click where you want to put "
                                     "the new instance"),
    ACTION_NEW_SD_MESSAGE        : _("Click where you want to put "
                                     "the new message"),
    ACTION_DEST_SD_MESSAGE       : _("Click on the destination of the message"),
    ACTION_NEW_IMPLEMENT_LINK    : a,
    ACTION_NEW_INHERIT_LINK      : a,
    ACTION_NEW_AGGREGATION_LINK  : a,
    ACTION_NEW_COMPOSITION_LINK  : a,
    ACTION_NEW_ASSOCIATION_LINK  : a,
    ACTION_NEW_NOTE_LINK         : a,
    ACTION_DEST_IMPLEMENT_LINK   : b,
    ACTION_DEST_INHERIT_LINK     : b,
    ACTION_DEST_AGGREGATION_LINK : b,
    ACTION_DEST_COMPOSITION_LINK : b,
    ACTION_DEST_ASSOCIATION_LINK : b,
    ACTION_DEST_NOTE_LINK        : b,

    # Patch from D.Dabrowsky, 20060129
    ACTION_ZOOM_IN               : _("Select the area to fit on"),
    ACTION_ZOOM_OUT              : _("Select the central point"),

}

del a, b


# Define current use mode
[SCRIPT_MODE, NORMAL_MODE] = assignID(2)


def getMediator():
    """
    Factory function to get the unique Mediator instance (singleton).

    @since 1.0
    @author L. Burgbacher <lb@alawa.ch>
    """
    return Mediator()

class Mediator(Singleton):
    """
    This class is the link between the parts of the GUI of pyut. It receives
    commands from the modules, and dispatch them to the right receiver.
    See the Model-View-Controller pattern and the Mediator pattern.
    There's just one instance of it, and it's global. You get the only
    instance by instanciating it. See the `singleton.py` file for more
    information about this.

    Each part of the GUI must register itself to the mediator. This is done
    with the various `register...` methods.

    The mediator contains a state machine. The different states are
    represented by integer constants, declared at the beginning of the
    `mediator.py` file. These are the `ACTION_*` constants.

    The `NEXT_ACTION` dictionary gives the next action based on the given
    one. For example, after an `ACTION_NEW_NOTE_LINK`, you get an
    `ACTION_DEST_NOTE_LINK` this way::

        nextAction = NEXT_ACTION[ACTION_NEW_NOTE_LINK]

    The state is kept in `self._currentAction`.

    The `doAction` is called whenever a click is received by the uml diagram
    frame.

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.38 $
    """
    def init(self):
        """
        Singleton constructor.

        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        @modified C.Dutoit 20021121 Added self._project
        """
        import ErrorManager
        self._errorManager = ErrorManager.getErrorManager()
        self._currentAction = ACTION_SELECTOR
        self._useMode = NORMAL_MODE # Define current use mode
        self._currentActionPersistent = False
        self._toolBar  = None # toolbar
        self._tools    = None # toolbar tools
        #self._uml      = None # current uml frame
        #self._project  = None # current project
        self._status   = None # application status bar
        self._src      = None # source of a two-objects action
        self._dst      = None # destination of a two-objects action
        self._appFrame = None # Application's main frame
        self._appPath  = None # Application files' path
        self.registerClassEditor(self.standardClassEditor)
        self._toolboxOwner = None # toolbox owner, created when appframe is passed
        self._fileHandling = None # File Handler
        #self.registerClassEditor(self.fastTextClassEditor)

        # Patch from D.Dabrowsky, 20060129
        self._modifyCommand = None  # command for undo/redo a modification on a shape.


    #>------------------------------------------------------------------
    def registerFileHandling(self, fh):
        self._fileHandling = fh

    #>------------------------------------------------------------------

    def setScriptMode(self):
        """
        Define the script mode, to use PyUt without graphical elements
        @author C.Dutoit
        """
        self._useMode = SCRIPT_MODE

    #>------------------------------------------------------------------

    def isInScriptMode(self):
        """
        True if the current mode is the scripting mode
        @author C.Dutoit
        """
        return self._useMode == SCRIPT_MODE

    #>------------------------------------------------------------------

    def getErrorManager(self):
        """
        Return the current error manager

        @author C.Dutoit
        """
        return self._errorManager

    #>------------------------------------------------------------------

    def registerFileHandling(self, fh):
        """
        Define the file handling class

        @param FileHandling fh : The FileHandling class to be used
        @author C.Dutoit
        """
        self._fileHandling = fh

    #>------------------------------------------------------------------

    def registerAppPath(self, path):
        """
        Register the path of the application files.

        @param string path
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._appPath = path

    #>------------------------------------------------------------------

    def getAppPath(self):
        """
        Return the path of the application files.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._appPath

    #>------------------------------------------------------------------

    def notifyTitleChanged(self):
        """
        Notify appframe that the application title has changed

        @since 1.27.2.23
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if not self._appFrame is None:
            self._appFrame.notifyTitleChanged()


    #>------------------------------------------------------------------

    def registerAppFrame(self, appFrame):
        """
        Register the application's main frame.

        @param wxFrame appFrame : Application's main frame
        @since 1.27.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._appFrame=appFrame
        if self._toolboxOwner == None:
            self._toolboxOwner = ToolboxOwner(appFrame)

    #>------------------------------------------------------------------

    def getAppFrame(self):
        """
        """
        return self._appFrame

    #>------------------------------------------------------------------

    def registerToolBar(self, tb):
        """
        Register the toolbar.

        @param wxToolbar tb : the toolbar
        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        """
        self._toolBar = tb

    #>------------------------------------------------------------------

    def registerToolBarTools(self, tools):
        """
        Register the toolbar tools.

        @param int[] tools : a list of the tools IDs
        @author L. Burgbacher
        """
        self._tools = tools

    #>------------------------------------------------------------------

    #def registerUMLFrame(self, uml):
        #"""
        #Register the Uml Frame.
#
        #@param wxWindow uml : the uml frame
        #@author L. Burgbacher
        #"""
        #self._uml = uml

    #>------------------------------------------------------------------

    #def registerCurrentProject(self, project):
        #"""
        #Register the current project
#
        #@param PyutProject project : the project
        #@author C.Dutoit
        #"""
        #self._project = project

    #>------------------------------------------------------------------

    def registerStatusBar(self, statusBar):
        """
        Register the status bar.

        @param wxStatusBar statusBar : the status bar
        @author L. Burgbacher
        """
        self._status = statusBar

    #>------------------------------------------------------------------

    def fastTextClassEditor(self, pyutClass):
        plugs = self._appFrame.plugs
        cl = [s for s in plugs.values()
            if s(None, None).getName() == "Fast text edition"]
        if cl:
            obj = cl[0](self.getUmlObjects(), self.getUmlFrame())
        else:
            # fallback
            self.standardClassEditor(pyutClass)
            return

        # Do plugin functionality
        wx.BeginBusyCursor()
        obj.callDoAction()
        wx.EndBusyCursor()
        self.getUmlFrame().Refresh()

    #>------------------------------------------------------------------

    def standardClassEditor(self, pyutClass):
        """
        The standard class editor dialogue, for registerClassEditor.

        @param PyutClass pyutClass : the class to edit
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        dlg = DlgEditClass(umlFrame, -1, pyutClass)
        dlg.Destroy()

    #>------------------------------------------------------------------

    def registerClassEditor(self, classEditor):
        """
        Register a function to invoque a class editor.
        This function takes one parameter, the pyutClass to edit.

        @param fct(PyutClass)
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.classEditor = classEditor

    #>------------------------------------------------------------------

    def setCurrentAction(self, action):
        """
        Set the new current atction.
        This tells the mediator which action to do for the next doAction call.

        @param int action : the action from ACTION constants
        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        """
        if self._currentAction==action:
            self._currentActionPersistent = True
        else:
            self._currentAction = action
            self._currentActionPersistent = False
        # put a message in the status bar
        self.setStatusText(MESSAGES[self._currentAction])

    #>------------------------------------------------------------------

    def doAction(self, x, y):
        """
        Do the current action at coordinates x, y.

        @param int x : x coord where the action must take place
        @param int y : y coord where the action must take place
        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        self.resetStatusText()
        if self._currentAction == ACTION_SELECTOR:
            return SKIP_EVENT
        elif self._currentAction == ACTION_NEW_CLASS:
            from createOglClassCommand import CreateOglClassCommand
            from commandGroup import CommandGroup
            cmd = CreateOglClassCommand(x, y, True)
            group = CommandGroup("Create class")
            group.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(group)
            umlFrame.getHistory().execute()

##            pyutClass = umlFrame.createNewClass(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
##            self.classEditor(pyutClass)
##            self.autoResize(pyutClass)
##            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_NOTE:
            pyutNote = umlFrame.createNewNote(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = DlgEditNote(umlFrame, -1, pyutNote)
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_ACTOR:
            pyutActor = umlFrame.createNewActor(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = wx.TextEntryDialog(umlFrame, "Actor name", "Enter actor name",
                    pyutActor.getName(), wx.OK | wx.CANCEL | wx.CENTRE)
            if dlg.ShowModal() == wx.ID_OK:
                pyutActor.setName(dlg.GetValue())
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_USECASE:
            pyutUseCase = umlFrame.createNewUseCase(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = DlgEditUseCase(umlFrame, -1, pyutUseCase)
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_SD_INSTANCE:
            try:
                from UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
                if not isinstance(umlFrame, UmlSequenceDiagramsFrame):
                    displayError(_("A SD INSTANCE can't be added to a " +
                                 "class diagram. You must create a sequence " +
                                 "diagram."))
                    return
                instance = umlFrame.createNewSDInstance(x, y)
                if not self._currentActionPersistent:
                    self._currentAction = ACTION_SELECTOR
                    self.selectTool(self._tools[0])
                dlg = wx.TextEntryDialog(umlFrame, "Instance name", "Enter instance name",
                        instance.getInstanceName(), wx.OK | wx.CANCEL | wx.CENTRE)
                if dlg.ShowModal() == wx.ID_OK:
                    instance.setInstanceName(dlg.GetValue())
                dlg.Destroy()
                umlFrame.Refresh()
            except:
                displayError(_("An error occured while trying to do this action"))
                umlFrame.Refresh()
        #added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (10.10.2005)
        elif self._currentAction == ACTION_ZOOM_IN:
            return SKIP_EVENT
        elif self._currentAction == ACTION_ZOOM_OUT:
            umlFrame.DoZoomOut(x, y)
            umlFrame.Refresh()
            self.updateTitle()
        else:
            return SKIP_EVENT
        return EVENT_PROCESSED

    #>------------------------------------------------------------------

    def selectTool(self, ID):
        """
        Select the tool of given ID from the toolbar, and delesect the others.

        @since 1.9
        @author L. Burgbacher <lb@alawa.ch>
        """
        for id in self._tools:
            self._toolBar.ToggleTool(id, False)
        self._toolBar.ToggleTool(ID, True)

#Added by P. Dabrowski (20051122) to change the cursor if we perform a zoom
#It's experimental, and must be redone to work with other os that WinXp
##        umlFrame = self.getFileHandling().getCurrentFrame()
##
##        from AppFrame import ID_ZOOMIN
##        from AppFrame import ID_ZOOMOUT
##        if ID == ID_ZOOMIN or ID == ID_ZOOMOUT:
##
##            from wx import Cursor
##            from wx import BITMAP_TYPE_CUR
##            zoomCursor = Cursor("img/MAGNIFY.CUR", BITMAP_TYPE_CUR)
##            umlFrame.SetCursor(zoomCursor)
##
##        else :
##
##            defaultCursor = umlFrame.getDefaultCursor()
##            umlFrame.SetCursor(defaultCursor)



    #>------------------------------------------------------------------

    def shapeSelected(self, shape, position = None):
        """
        Do action when a shape is selected.

        @since 1.9
        @author L. Burgbacher <lb@alawa.ch>
        @todo : support each link type
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        # do the right action
        if self._currentAction in SOURCE_ACTIONS:
            # get the next action needed to complete the whole action
            if self._currentActionPersistent:
                self._oldAction = self._currentAction
            self._currentAction = NEXT_ACTION[self._currentAction]

            # if no source, cancel action
            if shape is None:
                print(_("Action cancelled"), " (no source)")
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
                self.setStatusText(_("Action cancelled"))
            else: #store source
                self._src = shape
                self._srcPos = position
        elif self._currentAction in DEST_ACTIONS:
            # store the destination object
            self._dst = shape
            self._dstPos = position
            # if no destination, cancel action
            if self._dst is None:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
                self.setStatusText(_("Action cancelled"))
                return

            # create a link from source to destination
#            try:
            from createOglLinkCommand import CreateOglLinkCommand
            from commandGroup import CommandGroup
            cmd = CreateOglLinkCommand(self._src,
                                       self._dst,
                                       LINK_TYPE[self._currentAction],
                                       self._srcPos,
                                       self._dstPos)

            cmdGroup = CommandGroup("create link")
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            umlFrame.getHistory().execute()



            self._src = None
            self._dst = None
            if self._currentActionPersistent:
                self._currentAction = self._oldAction
                del self._oldAction
            else:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
        else:
            self.setStatusText(
                _("Error : Action not supported by the mediator"))
            return
        self.setStatusText(MESSAGES[self._currentAction])


    #>------------------------------------------------------------------

    def actionWaiting(self):
        """
        Return True if there's an action waiting to be completed.

        @since 1.2
        @author L. Burgbacher <lb@alawa.ch>
        """
        return self._currentAction != ACTION_SELECTOR

    #>------------------------------------------------------------------

    def autoResize(self, obj):
        """
        Autoresize the given object.

        @param PyutClass obj
        @param OglClass obj
        @since 1.18
        @author L. Burgbacher <lb@alawa.ch>
        """
        from OglClass import OglClass
        prefs=PyutPreferences()

        if prefs["AUTO_RESIZE"]:

            if isinstance(obj, PyutClass):
                #print "DBG-Autoresize"
                #print dir(obj)
                #print "getUmlObjects:", self.getUmlObjects()
                # get the associated oglClass and resize it
                po = [po for po in self.getUmlObjects()
                    if isinstance(po, OglClass) and po.getPyutObject() is obj]
                #print po
                obj = po[0]

            obj.autoResize()

    #>------------------------------------------------------------------

    def editObject(self, x, y):
        """
        Edit the object at x, y.

        @since 1.10
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        from OglClass import OglClass
        from OglNote  import OglNote
        from OglUseCase import OglUseCase
        from OglActor import OglActor
        from OglAssociation import OglAssociation
        #from OglInheritance import OglInheritance
        from OglInterface import OglInterface
        #print "mediator-editObject1", x, y
        object = umlFrame.FindShape(x, y)
        #print "mediator-editObject object=", object
        if object is None:
            return

        if isinstance(object, OglClass):
            pyutObject = object.getPyutObject()
            self.classEditor(pyutObject)
            self.autoResize(object)
        elif isinstance(object, OglNote):
            pyutObject = object.getPyutObject()
            dlg = DlgEditNote(umlFrame, -1, pyutObject)
            dlg.Destroy()
        elif isinstance(object, OglUseCase):
            pyutObject = object.getPyutObject()
            dlg = DlgEditUseCase(umlFrame, -1, pyutObject)
            dlg.Destroy()
        elif isinstance(object, OglActor):
            pyutObject = object.getPyutObject()
            dlg = wx.TextEntryDialog(umlFrame, "Actor name", "Enter actor name",
                    pyutObject.getName(), wx.OK | wx.CANCEL | wx.CENTRE)
            if dlg.ShowModal() == wx.ID_OK:
                pyutObject.setName(dlg.GetValue())
            dlg.Destroy()
        elif isinstance(object, OglAssociation):
            dlg = DlgEditLink(None, -1, object.getPyutObject())
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            dlg.Destroy()
            if rep == -1: # destroy link
                object.Detach()
                #self.removeLink(object)
        elif isinstance(object, OglInterface):
            dlg = DlgEditLink(None, -1, object.getPyutObject())
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            dlg.Destroy()
            if rep == -1: # destroy link
                object.Detach()
                #self.removeLink(object)

        umlFrame.Refresh()

    #>------------------------------------------------------------------

    def getUmlObjects(self):
        """
        Return the list of UmlObjects in the diagram.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        if self._fileHandling is None:
            return []
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is not None:
            return umlFrame.getUmlObjects()
        else:
            return []

    #>------------------------------------------------------------------

    def getSelectedShapes(self):
        """
        Return the list of selected OglObjects in the diagram.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlObjects = self.getUmlObjects()
        if umlObjects is not None:
            return [obj for obj in self.getUmlObjects() if obj.IsSelected()]
        else:
            return []

    #>------------------------------------------------------------------

    def setStatusText(self, msg):
        """
        Set the text in the status bar.

        @param String msg : The message to put in the status bar
        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        if msg is not None:
            self._status.SetStatusText(msg)

    #>------------------------------------------------------------------

    def resetStatusText(self):
        """
        Reset the text in the status bar.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        self._status.SetStatusText(_("Ready"))

    #>------------------------------------------------------------------

    def getDiagram(self):
        """
        Return the uml diagram.

        @since 1.12
        @return uml diagram if present, None otherwise
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return None
        return umlFrame.getDiagram()

    #>------------------------------------------------------------------

    def getUmlFrame(self):
        """
        Return the active uml frame.

        @return UmlFrame
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._fileHandling.getCurrentFrame()

    #>------------------------------------------------------------------

    def deselectAllShapes(self):
        """
        Deselect all shapes in the diagram.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is not None:
            shapes = umlFrame.GetDiagram().GetShapes()
            for shape in shapes:
                shape.SetSelected(False)
            umlFrame.Refresh()

    #>------------------------------------------------------------------

    def showParams(self, val):
        """
        Choose wether to show the params in the classes or not.

        @param bool int
        @since 1.17
        @author L. Burgbacher <lb@alawa.ch>
        """
        if val:
            PyutMethod.setStringMode(WITH_PARAMS)
        else:
            PyutMethod.setStringMode(WITHOUT_PARAMS)

    #>------------------------------------------------------------------

    # No longer used ?
    #def removeLink(self, link):
    #    """
    #    Remove a link from all referencing objects.

    #    @param OglLink link : link to remove
    #    @since 1.24
    #    @author L. Burgbacher <lb@alawa.ch>
    #    """
    #    # remove the link from the OglClasses
    #    try:
    #        link.getSourceShape().getLinks().remove(link)
    #    except ValueError:
    #        pass # could be already removed
    #    try:
    #        link.getDestinationShape().getLinks().remove(link)
    #    except ValueError:
    #        pass # could be already removed
    #    # remove the link from the source PyutClass
    #    from OglInheritance import OglInheritance
    #    if isinstance(link, OglInheritance):
    #        link.getSourceShape().getPyutObject().getFathers()\
    #            .remove(link.getPyutObject().getDestination())
    #    else:
    #        link.getSourceShape().getPyutObject().getLinks()\
    #            .remove(link.getPyutObject())
    #    # remove the link from the diagram
    #    link.Detach()
    #    self.getUmlObjects().remove(link)



    #>------------------------------------------------------------------

    #def removeClass(self, obj):
    #    """
    #    Remove an OglClass from the screen, without removing the links !

    #    @param OglClass obj : class to remove
    #    @since 1.24
    #    @author L. Burgbacher <lb@alawa.ch>
    #    """
    #    #obj.SetSelected(False)
    #    #self.getDiagram().RemoveShape(obj)
    #    obj.Detach()
    #    self.getUmlObjects().remove(obj)

    #>------------------------------------------------------------------

    #def getCurrentProject(self):
        #"""
        #Return the current project's instance
#
        #@return PyutProject the current project's instance
        #@author C.Dutoit
        #"""
        #return self._fileHandling.getCurrentProject()
        #return self._project

    #>------------------------------------------------------------------

    #def getCurrentDocument(self):
        #"""
        #Return the current project's document
#
        #@return PyutDocument
        #@author C.Dutoit
        #"""
        #return self._fileHandling.getCurrentDocument()

    #>------------------------------------------------------------------

    def getCurrentDir(self):
        """
        Return the application's current directory

        @return String : application's current directory
        """
        return self._appFrame.getCurrentDir()

    #>------------------------------------------------------------------

    def setCurrentDir(self, directory):
        """
        Set the application's current directory

        @param String directory : New appliation's current directory
        """
        return self._appFrame.updateCurrentDir(directory)

    #>------------------------------------------------------------------------

    def processChar(self, event):
        """
        Process the keyboard events.

        @param
        @return
        @since 1.0
        """
        c = event.GetKeyCode()
        funcs = {
            wx.WXK_DELETE : self.deleteSelectedShape,
            wx.WXK_INSERT : self.insertSelectedShape,
            ord('i')   : self.insertSelectedShape,
            ord('I')   : self.insertSelectedShape,
            ord('s')   : self.toggleSpline,
            ord('S')   : self.toggleSpline,
            ord('<')   : self.moveSelectedShapeDown,
            ord('>')   : self.moveSelectedShapeUp,
        }
        if funcs.has_key(c):
            funcs[c]()
        else:
            print("Not supported : ", c)
            event.Skip()

    #>------------------------------------------------------------------------

    def deleteSelectedShape(self):
        from delOglObjectCommand import DelOglObjectCommand
        from delOglClassCommand import DelOglClassCommand
        from delOglLinkCommand import DelOglLinkCommand
        from OglClass import OglClass
        from OglObject import OglObject
        from OglLink import OglLink
        from commandGroup import CommandGroup
        umlFrame = self._fileHandling.getCurrentFrame()
        # TODO : check this : if umlFrame is None: return
        selected = umlFrame.GetSelectedShapes()
        cmdGroup = CommandGroup("Delete UML object(s)")
        for shape in selected:
            cmd = None
            if isinstance(shape, OglClass):
                cmd = DelOglClassCommand(shape)
            elif isinstance(shape, OglObject):
                cmd = DelOglObjectCommand(shape)
            elif isinstance(shape, OglLink):
                cmd = DelOglLinkCommand(shape)

        #if the shape is not an Ogl instance no command has
        #been created.
            if cmd is not None :
                cmdGroup.addCommand(cmd)
                cmdGroupInit = True
            else :
                shape.Detach()
                umlFrame.Refresh()

        if cmdGroupInit:
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            umlFrame.getHistory().execute()



##        from OglClass        import OglClass
##        umlFrame = self._fileHandling.getCurrentFrame()
##        if umlFrame is None: return
##        selected = umlFrame.GetSelectedShapes()
##        for shape in selected:
##            if isinstance(shape, OglClass):
##                # need to check if the class has children, and remove the
##                # refs in the children
##                pyutClass = shape.getPyutObject()
##                for klass in [s.getPyutObject() for s in self.getUmlObjects()
##                    if isinstance(s, OglClass)]:
##                    if pyutClass in klass.getFathers():
##                        klass.getFathers().remove(pyutClass)
##            shape.Detach()
##        umlFrame.Refresh()


    #>------------------------------------------------------------------------

    def insertSelectedShape(self):
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        selected = umlFrame.GetSelectedShapes()
        if len(selected) != 1:
            return
        selected = selected.pop()
        if isinstance(selected, LinePoint):
            px, py = selected.GetPosition()
            # add a control point and make it child of the shape if it's a
            # self link
            line = selected.GetLines()[0]
            if line.GetSource().GetParent() is \
                line.GetDestination().GetParent():
                cp = ControlPoint(0, 0, line.GetSource().GetParent())
                cp.SetPosition(px + 20, py + 20)
            else:
                cp = ControlPoint(px + 20, py + 20)
            line.AddControl(cp, selected)
            umlFrame.GetDiagram().AddShape(cp)
            umlFrame.Refresh()

    #>------------------------------------------------------------------------

    def toggleSpline(self):
        from OglLink         import OglLink
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        selected = umlFrame.GetSelectedShapes()
        for shape in selected:
            if isinstance(shape, OglLink):
                shape.SetSpline(not shape.GetSpline())
        umlFrame.Refresh()

    #>------------------------------------------------------------------------

    def moveSelectedShapeUp(self):
        """
        Move the selected shape one level up in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        self._moveSelectedShapeZOrder(umlFrame.GetDiagram().MoveToFront)

    #>------------------------------------------------------------------------

    def moveSelectedShapeDown(self):
        """
        Move the selected shape one level down in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        self._moveSelectedShapeZOrder(umlFrame.GetDiagram().MoveToBack)

    #>------------------------------------------------------------------------

    def _moveSelectedShapeZOrder(self, callback):
        """
        Move the selected shape one level in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import OglObject
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        selected = umlFrame.GetSelectedShapes()
        if len(selected)>0:
            for object in selected:
                if isinstance(object, OglObject.OglObject):
                    callback(object)
        umlFrame.Refresh()


    #>------------------------------------------------------------------------

    def registerTool(self, tool):
        """
        Add a tool to toolboxes

        @param Tool tool : The tool to add
        @since 1.3
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._toolboxOwner.registerTool(tool)


    #>------------------------------------------------------------------------

    def displayToolbox(self, category):
        """
        Display a toolbox

        @param String category : category of tool to display
        @since 1.3
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._toolboxOwner.displayToolbox(category)

    #>------------------------------------------------------------------------
    def getToolboxesCategories(self):
        """
        Return all categories of toolboxes

        @return string[] of categories
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._toolboxOwner.getCategories()


    #>------------------------------------------------------------------------

    def getOglClass(self, pyutClass):
        """
        Return an OGLClass instance corresponding to a pyutClass

        @param pyutClass : the pyutClass to get OGLClass
        @return OGLClass
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        from OglClass import OglClass
        po = [po for po in self.getUmlObjects()
            if isinstance(po, OglClass) and po.getPyutObject() is pyutClass]
        return po[0]



    #>------------------------------------------------------------------------

    #def getProjectFromUmlFrame(self, umlFrame):
        #"""
        #Get a project to which a specified umlFrame belongs
#
        #@param umlFrame : the umlFrame
        #@return Project : the project that owns umlFrame or None if not foud
        #@author C.Dutoit
        #"""
        #for project in self._fileHandling.getProjects():
            #for frame in [document.getFrame()
                          #for document in project.getDocuments()]:
                #if frame is umlFrame:
                    #return project
        #return None


    #>------------------------------------------------------------------------

    def getFileHandling(self):
        """
        Return the FileHandling class

        @return FileHandling instance
        @author C.Dutoit
        """
        return self._fileHandling


    #>------------------------------------------------------------------------

    def updateTitle(self):
        """
        Set the application title, fonction of version and current filename

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Exit if we are in scripting mode
        if self.isInScriptMode():
            return

        # Get filename
        project = self._fileHandling.getCurrentProject()
        if project is not None:
            filename = project.getFilename()
        else:
            filename = ""

        #Set text
        txt = "PyUt v" + __PyUtVersion__ + " - " + filename
        if (project is not None) and (project.getModified()):
            if self._fileHandling.getCurrentFrame() is not None:
                zoom = self._fileHandling.getCurrentFrame().GetCurrentZoom()
            else:
                zoom = 1

            txt=txt + " (" + ((int)(zoom * 100)).__str__() + "%)" + " *"
        self._appFrame.SetTitle(txt)

    #>------------------------------------------------------------------------

    def loadByFilename(self, filename):
        """
        Load a file from its filename
        @author C.Dutoit
        """
        self._appFrame.loadByFilename(filename)

    #>------------------------------------------------------------------------

    def cutSelectedShapes(self):
        self._appFrame.cutSelectedShapes()

    #>------------------------------------------------------------------------

    def getCurrentAction(self):
        return self._currentAction

    #>------------------------------------------------------------------------

    def beginChangeRecording(self, oglObject):

        from delOglClassCommand import DelOglClassCommand
        from delOglObjectCommand import DelOglObjectCommand
        from delOglLinkCommand import DelOglLinkCommand
        from OglClass import OglClass
        from OglLink import OglLink
        from OglObject import OglObject

        if isinstance(oglObject, OglClass):
            print("begin")
            self._modifyCommand = DelOglClassCommand(oglObject)
        elif isinstance(oglObject, OglLink):
            self._modifyCommand = DelOglLinkCommand(oglObject)
        elif isinstance(oglObject, OglObject):
            self._modifyCommand = DelOglObjectCommand(oglObject)
        else:
            raise RuntimeError("a non-OglObject has requested for a change recording")

    #>------------------------------------------------------------------------

    def endChangeRecording(self, oglObject):

        from createOglClassCommand import CreateOglClassCommand
        from OglClass import OglClass
        from OglLink import OglLink
        from OglObject import OglObject
        from commandGroup import CommandGroup

        cmd = None

        if isinstance(oglObject, OglClass):
            print("end")
            cmd = CreateOglClassCommand(shape = oglObject)


        if cmd is not None and self._modifyCommand is not None :

            group = CommandGroup("modify " + oglObject.getPyutObject().getName())
            group.addCommand(self._modifyCommand)
            group.addCommand(cmd)

            umlFrame = self.getFileHandling().getCurrentFrame()
            umlFrame.getHistory().addCommandGroup(group)

        cmd = None
        self._modifyCommand = None

