#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "$Revision: 1.4 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-02-13"

from glob import glob
import os, sys

# needed by the plugins
from PyutClass      import PyutClass
from PyutParam      import PyutParam
from PyutMethod     import PyutMethod
from PyutField      import PyutField
from PyutStereotype import PyutStereotype
from UmlFrame       import *
from OglClass       import OglClass
from OglLink        import *
from singleton      import Singleton

class PluginManager(Singleton):
    """
    Interface between the application and the plugins.

    This class is responsible to search for available plugins, load them,
    extract runtime information and give the information to those who need it
    (for example the `AppFrame` to create the import/export submenus).

    @author Laurent Burgbacher <lb@alawa.ch>
    @version $Revision: 1.4 $

    @modified C.Dutoit <dutoitc@hotmail.com> oct02, added ToPlugins
    """
    def init(self):
        """
        Singleton Constructor.
        At init time, this class searches for the plugins in the plugins
        directory.

        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Init
        self.ioPlugs = []
        self.toPlugs = []

        # get the file names
        os.chdir("plugins")
        sys.path.append(os.getcwd())
        ioPlugs = glob("Io*.py")
        toPlugs = glob("To*.py")
        os.chdir(os.pardir)

        # remove extension
        ioPlugs = map(lambda x: os.path.splitext(x)[0], ioPlugs)
        toPlugs = map(lambda x: os.path.splitext(x)[0], toPlugs)

        # Import I/O plugins
        for plug in ioPlugs:
            print("Importing I/O plugin from file " + str(plug))
            module = None
            #~ module = __import__(plug)
            try:
                module = __import__(plug)
            except:
                print(("Error importing plugin %s with message:" % plug))
                import traceback
                print("Error : %s" % sys.exc_info()[0])
                print("Msg   : %s" % sys.exc_info()[1])
                print("Trace :")
                for el in traceback.extract_tb(sys.exc_info()[2]):
                    print(el)
            if module is not None:
                cl = eval("module.%s" % (module.__name__))
                self.ioPlugs.append(cl)

        # Import tools plugins
        for plug in toPlugs:
            print("Importing tool plugin from file " + str(plug))
            module = None
            #~ module = __import__(plug)
            try:
                module = __import__(plug)
            except:
                print(("Error importing plugin %s with message:" % plug))
                import traceback
                print("Error : %s" % sys.exc_info()[0])
                print("Msg   : %s" % sys.exc_info()[1])
                print("Trace :")
                for el in traceback.extract_tb(sys.exc_info()[2]):
                    print(el)
            if module is not None:
                cl = eval("module.%s" % (module.__name__))
                self.toPlugs.append(cl)



    #>------------------------------------------------------------------------

    def getPluginsInfo(self):
        """
        Get textual information about available plugins.

        @return String []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        s = []
        for plug in self.ioPlugs + self.toPlugs:
            obj = plug(None, None)
            s.append("Plugin : %s version %s (c) by %s" % (
                obj.getName(), obj.getVersion(), obj.getAuthor()))
        return s

    #>------------------------------------------------------------------------

    def getInputPlugins(self):
        """
        Get the input plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        list = []
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getInputFormat() is not None:
                list.append(plug)
        return list

    #>------------------------------------------------------------------------

    def getOutputPlugins(self):
        """
        Get the output plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        list = []
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                list.append(plug)
        return list

    #>------------------------------------------------------------------------
    
    def getToolPlugins(self):
        """
        Get the tool plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.5.2.6
        """
        return self.toPlugs
        #list = []
        #for plug in self.toPlugs:
        #    obj = plug(None, None)
        #    list.append(plug)
        #return list
    
    #>------------------------------------------------------------------------

def test():
    p = PluginManager()
    for info in p.getPluginsInfo():
        print(info)

if __name__ == "__main__": test()
