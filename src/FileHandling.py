#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.35 $"
__author__  = "EI6, eivd, Group Dutoit - Roux"
__date__    = "2002-03-14"
__PyUtVersion__ = "1.0"

#from wxPython.wx import *
from UmlClassDiagramsFrame import UmlClassDiagramsFrame
from AppFrame import *
from pyutUtils import displayError
from PyutProject import PyutProject
from PyutDocument import PyutDocument
import PyutConsts, wx



#>-----------------------------------------------------------------------

def shorterFilename(filename):
    """
    Return a shorter filename to display

    @param filename file name to display
    @return String better file name
    @since 1.0
    @author C.Dutoit <dutoitc@hotmail.com>
    """
    import os
    str = os.path.split(filename)[1]
    if len(str)>12:
        return str[:4] + str[-8:]
    else:
        return str

##############################################################################

class FileHandling:
    """
    FileHandling : Handle files in Pyut
    Used by AppFrame to contain all UML frames, the notebook and 
    the project tree.
    
    All actions called from AppFrame are executing on the current frame

    AppFrame use the following methods :
        - getProjects() : boolean
        - isProjectLoaded(filename) : boolean
        - isDefaultFilename(filename) : boolean
        - openFile(filename)
        - insertFile(filename)
        - saveFile()
        - saveFileAs()
        - newProject()
        - newDocument()
        - exportToImageFile(self, extension, imageType)
        - setModified(self, flag=True)
        - closeCurrentProject(self)

    Others methods are internal and called only by this module (and they are
    private !)

    :author: C.Dutoit 
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.35 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent, mediator):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._projects = []
        self.__parent = parent
        self._ctrl = mediator # PyUt mediator
        self._currentProject = None
        self._currentFrame = None

        # Init graphic
        if not self._ctrl.isInScriptMode():
            self._initGraphicalElements()

        #self._ctrl.registerUMLFrame(None)

    #>-----------------------------------------------------------------------

    def registerUmlFrame(self, frame):
        """
        Register the current UML Frame
        """
        self._currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)

    #>------------------------------------------------------------------------

    def _initGraphicalElements(self):
        """
        Define all graphical elements
        @author C.Dutoit
        """
        # window splitting
        self.__splitter = wx.SplitterWindow(self.__parent, -1)

        # project tree
        self.__projectTree = wx.TreeCtrl(self.__splitter, -1, 
                                        style = wx.TR_HIDE_ROOT +
                                                wx.TR_HAS_BUTTONS)
        self.__projectTreeRoot=self.__projectTree.AddRoot(_("Root"))
        #self.__projectTree.SetPyData(self.__projectTreeRoot, None)
        # Expand root, since wx.TR_HIDE_ROOT is not supported under winx
        # Not supported for hidden tree since wx.Python 2.3.3.1 ?
        #self.__projectTree.Expand(self.__projectTreeRoot)

        # diagram container
        self.__notebook=wx.Notebook(self.__splitter, -1, style=wx.CLIP_CHILDREN)

        # Set splitter
        self.__splitter.SetMinimumPaneSize(20)
        #self.__splitter.SplitVertically(self.__projectTree, self.__notebook)
        #self.__splitter.SetSashPosition(100)
        self.__splitter.SplitVertically(self.__projectTree, self.__notebook, 160)


        # ...
        self.__notebookCurrentPage=-1

        # Callbacks
        self.__parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, 
                                  self.__onNotebookPageChanged)
        self.__parent.Bind(wx.EVT_TREE_SEL_CHANGED,
                             self.__onProjectTreeSelChanged)

    #>------------------------------------------------------------------------

    def showFrame(self, frame):
        self._frame = frame
        frame.Show()
    
    #>------------------------------------------------------------------------

    def getProjects(self):
        """
        Return all projects

        @return PyutProject[] the projects
        @author C.Dutoit
        """
        return self._projects
    
    #>------------------------------------------------------------------------

    def isProjectLoaded(self, filename):
        """
        Return True if the project is already loaded
        @author C.Dutoit
        """
        for project in self._projects:
            if project.getFilename == filename:
                return True
        return False

    #>------------------------------------------------------------------------

    def isDefaultFilename(self, filename):
        """
        Return True if the filename is the default filename
        """
        return filename==PyutConsts.DefaultFilename
    
    #>------------------------------------------------------------------------

    def openFile(self, filename, project = None):
        """
        Open a file

        @param String filename
        @return True if succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        #print ">>>FileHandling-openFile-1"
        # Exit if the file is already loaded
        if not self.isDefaultFilename(filename)\
           and self.isProjectLoaded(filename):
            displayError(_("The selected file is already loaded !"))
            return False
        #print ">>>FileHandling-openFile-2"
     
        # Create a new project ?
        if project is None:
            project = PyutProject(PyutConsts.DefaultFilename, self.__notebook, 
                                  self.__projectTree, self.__projectTreeRoot)

        #print ">>>FileHandling-openFile-3"
        # Load the project and add it
        try:
            if not project.loadFromFilename(filename):
                displayError(_("The specified file can't be loaded !"))
                return False
            self._projects.append(project)
            #self._ctrl.registerCurrentProject(project)
            self._currentProject = project
        except:
            displayError(_("An error occured while loading the project !"))
            return False

        #print ">>>FileHandling-openFile-4"
        try:
            for document in project.getDocuments():
                if not self._ctrl.isInScriptMode():
                    self.__notebook.AddPage(document.getFrame(),
                                            document.getDiagramTitle())
            #print ">>>FileHandling-openFile-5"
            if not self._ctrl.isInScriptMode():
                self.__notebookCurrentPage = self.__notebook.GetPageCount()-1
                self.__notebook.SetSelection(self.__notebookCurrentPage)
            #print ">>>FileHandling-openFile-6"
            if len(project.getDocuments())>0:
                self._currentFrame = project.getDocuments()[0].getFrame()
            #print ">>>FileHandling-openFile-7"
        except:
            displayError(_("An error occured while adding " +
                           "the project to the notebook"))
            return False


        #print ">>>FileHandling-openFile-8"
        return True

    #>-----------------------------------------------------------------------

    def insertFile(self, filename):
        """
        Insert a file in the current project

        @param filename : filename of the project to insert
        @author C.Dutoit
        """
        # Get current project
        project = self._currentProject

        # Save number of initial documents
        nbInitialDocuments = len(project.getDocuments())

        # Load datas... 
        if not project.insertProject(filename):
            displayError(_("The specified file can't be loaded !"))
            return False

        # ...
        if not self._ctrl.isInScriptMode():
            try:
                for document in project.getDocuments()[nbInitialDocuments:]:
                    self.__notebook.AddPage(document.getFrame(),
                                            document.getDiagramTitle())

                self.__notebookCurrentPage = self.__notebook.GetPageCount()-1
                self.__notebook.SetSelection(self.__notebookCurrentPage)
            except:
                displayError(_("An error occured while adding " +
                               "the project to the notebook"))
                return False
                
        # Select first frame as current frame
        if len(project.getDocuments())>nbInitialDocuments:
            self._frame = projects.getDocuments()[nbInitialDocuments].getFrame()

    #>-----------------------------------------------------------------------

    def saveFile(self):
        """
        save to the current filename

        @return bool True if succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        currentProject = self._currentProject
        if currentProject == None:
            displayError(_("No diagram to save !"), _("Error"))
            return

        if currentProject.getFilename() is None  \
                or currentProject.getFilename()==PyutConsts.DefaultFilename:
            return self.saveFileAs()
        else:
            return currentProject.saveXmlPyut()

    #>-----------------------------------------------------------------------

    def saveFileAs(self):
        """
        Ask for a filename and save datas to it.

        @return bool True if succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._ctrl.isInScriptMode():
            displayError(_("Save File As is not accessible in script mode !"))
            return
        
        # Test if no diagram exists
        if self._ctrl.getDiagram() is None:
            displayError(_("No diagram to save !"), _("Error"))
            return


        # Ask for filename
        filenameOK = False
        while not filenameOK:
            dlg=wx.FileDialog(self.__parent,
                    defaultDir=self.__parent.getCurrentDir(),
                    wildcard=_("Pyut file (*.put)|*.put"),
                    style=wx.SAVE | wx.OVERWRITE_PROMPT)

            # Return False if canceled
            if dlg.ShowModal() != wx.ID_OK:
                dlg.Destroy()
                return False


            # Find if a specified filename is already opened
            filename = dlg.GetPath()

            if len([project for project in self._projects 
                        if project.getFilename() == filename])>0:
                dlg = wx.MessageDialog(self.__parent, 
                    _("Error ! The filename '%s" +
                      "' correspond to a project which is currently opened !" +
                      " Please choose another filename !") %
                      str(filename),
                    _("Save change, filename error"),
                    wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return
            filenameOK = True

        #...
        project = self._currentProject
        project.setFilename(dlg.GetPath())
        project.saveXmlPyut()

        # Modify notebook text
        for i in range(self.__notebook.GetPageCount()):
            frame = self.__notebook.GetPage(i)
            document = [document for document in project.getDocuments()
                                 if document.getFrame() is frame]
            if len(document)>0:
                document=document[0]
                if frame in project.getFrames():
                    self.__notebook.SetPageText(i, document.getDiagramTitle())
            else:
                print "Not updating notebook in FileHandling"

        self.__parent.updateCurrentDir(dlg.GetPath())

        project.setModified(False)
        dlg.Destroy()
        return True

    #>-----------------------------------------------------------------------

    def newProject(self):
        """
        Begin a new project

        @author C.Dutoit
        """
        project = PyutProject(PyutConsts.DefaultFilename, self.__notebook, 
                              self.__projectTree, self.__projectTreeRoot)
        self._projects.append(project)
        self._currentProject = project
        self._currentFrame = None

    #>-----------------------------------------------------------------------

    def newDocument(self, type):
        """
        Begin a new document

        @param type : Type of document; one cited in PyutConsts.py
        @author C.Dutoit
        """
        project = self._currentProject
        if project is None:
            self.newProject()
            project = self.getCurrentProject()
        frame = project.newDocument(type).getFrame()
        self._currentFrame = frame
        self._currentProject = project

        if not self._ctrl.isInScriptMode():
            self.__notebook.AddPage(frame,
                                    shorterFilename(project.getFilename()))
            self.__notebookCurrentPage=self.__notebook.GetPageCount()-1
            self.__notebook.SetSelection(self.__notebookCurrentPage)

    #>-----------------------------------------------------------------------

    def exportToImageFile(self, extension, imageType):
        """
        Export the current diagram to an image file
        @author C.Dutoit
        """
        # Exit if in scripting mode
        if self._ctrl.isInScriptMode():
            displayError(_("Export to image file is not implemented in "
                           "scripting mode now !"))
            return

        dlg=wx.FileDialog(self.__parent, _("Export to %s file format" % extension),
                self.__parent.getCurrentDir(), "", "*." + extension,
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            # Deselect all shapes
            self._ctrl.deselectAllShapes()

            # Get frame
            frame = self.getCurrentFrame()

            # Get boundaries
            (x1, y1, x2, y2) = frame.getObjectsBoundaries()
            x2+=1
            y2+=1

            # Get output vars
            out_dc = wx.MemoryDC()
            out_bitmap = wx.EmptyBitmap(x2-x1, y2-y1)
            out_dc.SelectObject(out_bitmap)

            # Get input vars
            diag_dc = wx.MemoryDC()
            w, h = frame.GetVirtualSize()
            diag_dc.SelectObject(wx.EmptyBitmap(w, h))
            diag_dc.SetBackground(wx.WHITE_BRUSH)
            diag_dc.Clear()

            # Redraw and copy
            #frame.GetDiagram().Refresh(diag_dc)
            frame.Redraw(diag_dc)
            out_dc.BeginDrawing()
            out_dc.Blit(0, 0, x2-x1, y2-y1, diag_dc, x1, y1)
            out_dc.EndDrawing()
            out_dc.SelectObject(wx.NullBitmap);
            diag_dc.SelectObject(wx.NullBitmap);
            image = wx.ImageFromBitmap(out_bitmap)
            image.SaveFile(dlg.GetPath(), imageType)
        self.__parent.updateCurrentDir(dlg.GetPath())
        dlg.Destroy()
    
    #>-----------------------------------------------------------------------

    def exportToBmp(self, event):
        """
        Export the current diagram to bitmap

        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Exit if in scripting mode
        if self._ctrl.isInScriptMode():
            displayError(_("Export to bitmap file is not implemented in "
                           "scripting mode now !"))
            return

        self.exportToImageFile("bmp", wx.BITMAP_TYPE_BMP)


    #>-----------------------------------------------------------------------

    def exportToJpg(self, event):
        """
        Export the current diagram to a jpeg file

        @author C.Dutoit
        """
        self.exportToImageFile("jpg", wx.BITMAP_TYPE_JPEG)

    #>-----------------------------------------------------------------------

    def exportToPng(self, event):
        """
        Export the current diagram to a png file

        @author C.Dutoit
        """
        self.exportToImageFile("png", wx.BITMAP_TYPE_PNG)

    #>-----------------------------------------------------------------------

    def exportToPostscript(self, event):
        """
        Export the current diagram to postscript

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dlg = wx.MessageDialog(self.__parent, 
            _("Not yet implemented !"),
            _("Sorry..."),
            wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()
        return


        dlg=wx.FileDialog(self.__parent, _("Choose a file"),
                self.__parent.getCurrentDir(), "", "*.ps",
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            frame = self.getCurrentFrame()

            # Deselect all shapes
            self._ctrl.deselectAllShapes()

            # Get boundaries
            (x1, y1, x2, y2) = frame.getObjectsBoundaries()

            # Define printdata
            printData = wx.PrintData()
            printData.SetFilename(dlg.GetPath())

            # Get output vars
            out_dc = wx.PostScriptDC(printData)
            #out_bitmap = wx.EmptyBitmap(x2-x1, y2-y1)
            #out_dc.SelectObject(out_bitmap)
            printData.SetPrinterScaleX(x2-x1)
            printData.SetPrinterScaleY(y2-y1)
            #print dir(out_dc)

            # Get input vars
            diag_dc = wx.MemoryDC()
            w, h = self.getCurrentFrame().GetVirtualSize()
            diag_dc.SelectObject(wx.EmptyBitmap(w, h))
            diag_dc.SetBackground(wx.WHITE_BRUSH)
            diag_dc.Clear()

            # Redraw and copy
            frame.GetDiagram().Refresh(diag_dc)
            out_dc.BeginDrawing()
            out_dc.Blit(0, 0, x2-x1, y2-y1, diag_dc, x1, y1)
            out_dc.EndDrawing()
            out_dc.EndDoc()
            #out_dc.SelectObject(wx.NullBitmap);
            diag_dc.SelectObject(wx.NullBitmap);
            #image = wx.ImageFromBitmap(out_bitmap)
            #image.SaveFile(dlg.GetPath(), wx.BITMAP_TYPE_JPEG)

            #printer = wx.Printer(printData)
            #printer.print(frame, wx.PrintOut("..."), False))
        dlg.Destroy()
        return



    #>------------------------------------------------------------------------

    def __onNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.0
        """
        self.__notebookCurrentPage=self.__notebook.GetSelection()
        if not self._ctrl is None:
            #self._ctrl.registerUMLFrame(self._getCurrentFrame())
            self._currentFrame = self._getCurrentFrameFromNotebook()
            self.__parent.notifyTitleChanged()
        #self.__projectTree.SelectItem(getID(self.getCurrentFrame()))
        # TODO : how can I do getID ???

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self._currentFrame)

    #>------------------------------------------------------------------------

    def __onProjectTreeSelChanged(self, event):
        """
        Callback for notebook page changed

        @author C.Dutoit
        """
        pyData = self.__projectTree.GetPyData(event.GetItem())
        if isinstance(pyData, wx.ScrolledWindow):
            frame = pyData
            self._currentFrame = frame
            self._currentProject = self.getProjectFromFrame(frame)

            # Select the frame in the notebook
            for i in range(self.__notebook.GetPageCount()):
                pageFrame=self.__notebook.GetPage(i)
                if pageFrame is frame:
                    self.__notebook.SetSelection(i)
                    return
        elif isinstance(pyData, PyutProject):
            self._currentProject = pyData


    #>------------------------------------------------------------------------

    def _getCurrentFrameFromNotebook(self):
        """
        Get the current frame in the notebook

        @return frame Current frame in the notebook; -1 if none selected
        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.0
        """
        # Return None if we are in scripting mode
        if self._ctrl.isInScriptMode():
            return None

        noPage = self.__notebookCurrentPage
        if noPage == -1:
            return None
        frame = self.__notebook.GetPage(noPage)
        return frame

    #>-----------------------------------------------------------------------
    
    def getCurrentFrame(self):
        """
        Get the current frame
        @author C.Dutoit
        """
        return self._currentFrame
    
    #>-----------------------------------------------------------------------

    def getCurrentProject(self):
        """
        Get the current working project 

        @return Project : the current project or None if not found
        @author C.Dutoit
        """
        return self._currentProject
        #return self._getProjectFromFrame(self._currentFrame)

    #>-----------------------------------------------------------------------

    def getProjectFromFrame(self, frame):
        """
        Return the project that owns a given frame

        @param wx.Frame frame : the frame to get his project
        @return PyutProject or None if not found
        @author C.Dutoit
        """
        for project in self._projects:
            if frame in project.getFrames():
                return project
        return None


    #>-----------------------------------------------------------------------

    def getCurrentDocument(self):
        """
        Get the current document.

        @return PyutDocument : the current document or None if not found
        @author C.Dutoit
        """
        project = self.getCurrentProject()
        if project is None: return None
        for document in project.getDocuments():
            if document.getFrame() is self._currentFrame:
                return document
        return None


    #>-----------------------------------------------------------------------

    def onClose(self):
        """
        Close all files

        @return True if everything's ok
        @author C.Dutoit
        """
        # Display warning if we are in scripting mode
        if self._ctrl.isInScriptMode():
            print "WARNING : in script mode, the non-saved projects " \
                  "are closed without warning"

        # Close projects and ask for unsaved but modified projects
        if not self._ctrl.isInScriptMode():
            for project in self._projects:
                if project.getModified()==True:
                    frames = project.getFrames()
                    if len(frames)>0:
                        frame = frames[0]
                        frame.SetFocus()
                        wx.Yield()
                        #if self._ctrl is not None:
                            #self._ctrl.registerUMLFrame(frame)
                        self.showFrame(frame)
                    dlg = wx.MessageDialog(self.__parent, 
                        _("Your diagram has not been saved! Would you like to save it ?"),
                        _("Save changes ?"),
                        wx.YES_NO | wx.ICON_QUESTION)
                    if dlg.ShowModal()==wx.ID_YES:
                        #save
                        if self.saveFile()==False:
                            return False
                    dlg.Destroy()

        # Unreference all
        self.__parent = None
        self._ctrl = None
        self.__splitter = None
        self.__projectTree = None
        self.__notebook.DeleteAllPages()
        self.__notebook = None
        self.__splitter = None
        self._projects = None
        self._currentProject = None
        self._currentFrame = None

    #>-----------------------------------------------------------------------

    def setModified(self, flag=True):
        """
        Set the Modified flag of the currently opened diagram

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._currentProject is not None:
            self._currentProject.setModified(flag)
        self._ctrl.updateTitle()


    #>-----------------------------------------------------------------------

    def closeCurrentProject(self):
        """
        Close the current project

        @return True if everything's ok
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # No frame left ?
        if self._currentProject is None and self._currentFrame is not None:
            self._currentProject = self.getProjectFromFrame(self._currentFrame)
        if self._currentProject is None:
            displayError(_("No frame to close !"), _("Error..."))
            return

        # Display warning if we are in scripting mode
        if self._ctrl.isInScriptMode():
            print "WARNING : in script mode, the non-saved projects " \
                  "are closed without warning"

        # Close the file
        if self._currentProject.getModified()==True  \
           and not self._ctrl.isInScriptMode():
            # Ask to save the file
            frame = self._currentProject.getFrames()[0]
            frame.SetFocus()
            #self._ctrl.registerUMLFrame(frame)
            self.showFrame(frame)

            dlg = wx.MessageDialog(self.__parent, 
                _("Your project has not been saved. "
                  "Would you like to save it ?"),
                _("Save changes ?"),
                wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                #save
                if self.saveFile() == False:
                    return False

        # Remove the frame in the notebook
        if not self._ctrl.isInScriptMode():
            pages = range(self.__notebook.GetPageCount())
            pages.reverse()
            for i in pages:
                pageFrame=self.__notebook.GetPage(i)
                if pageFrame in self._currentProject.getFrames():
                    self.__notebook.DeletePage(i)
                    # RemovePage si erreur ??

        # Select a new notebook sheet
        #if self.__notebook.GetPageCount() > 0:
            #self.__notebookCurrentPage = 0
            #self.__notebook.SetSelection(self.__notebookCurrentPage)
        #else:
            #self.__notebookCurrentPage = -1
            #self.newFile(-1)                    # Create a new diagram
            #self.__notebookCurrentPage = 0
            #self.__notebook.SetSelection(self.__notebookCurrentPage)
            ##~ self._ctrl.registerUMLFrame(self.getCurrentFrame())
            #self.__parent.notifyTitleChanged()
        #self._ctrl.registerUMLFrame(None)
        #self._ctrl.registerCurrentProject(None)

        # Remove the frame in the tree
        #self._currentProject.removeFromNotebook()
        self._currentProject.removeFromTree()
        self._projects.remove(self._currentProject)
        #del project

        self._currentProject = None
        self._currentFrame = None


    #>-----------------------------------------------------------------------

    def removeAllReferencesToUmlFrame(self, umlFrame):
        """
        Remove all my references to a given uml frame

        @author C.Dutoit
        """
        # Current frame ?
        if self._currentFrame is umlFrame:
            self._currentFrame is None

        # Exit if we are in scripting mode
        if self._ctrl.isInScriptMode():
            return
        
        for i in range(self.__notebook.GetPageCount()):
            pageFrame = self.__notebook.GetPage(i)
            if pageFrame is umlFrame:
                self.__notebook.DeletePage(i)
                break


    #>-----------------------------------------------------------------------

    def getProjectFromOglObjects(self, oglObjects):
        """
        Get a project that owns oglObjects
       
        @param oglObjects Objects to find their parents
        @return PyutProject if found, None else
        @author C.Dutoit
        """
        for project in self._projects:
            for frame in project.getFrames():
                diagram = frame.getDiagram()
                shapes = diagram.GetShapes()
                for obj in oglObjects:
                    if obj in shapes:
                        return project
        return None
