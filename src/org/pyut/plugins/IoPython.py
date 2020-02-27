
from typing import List

from logging import Logger
from logging import getLogger

import os
from sys import path as sysPath

import wx

import importlib

from org.pyut.ogl.OglClass import OglClass

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.PyutUtils import PyutUtils

from org.pyut.plugins.PluginAst import FieldExtractor
from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin

from org.pyut.general.Globals import _

MaxWidth = 80

[ID_BTN_TO_THE_RIGHT, ID_BTN_TO_THE_LEFT] = PyutUtils.assignID(2)


class DlgAskWhichClassesToReverse(wx.Dialog):
    def __init__(self, lstClasses):
        wx.Dialog.__init__(self, None, -1, "Classes choice", style=wx.CAPTION | wx.RESIZE_BORDER, size=(400, 500))

        # Create not chosen classes listBox
        self._listBox1 = wx.ListBox(self, -1, style=wx.LB_EXTENDED | wx.LB_ALWAYS_SB | wx.LB_SORT, size=(320, 400))
        for klass in lstClasses:
            self._listBox1.Append(klass.__name__, klass)

        # Create chosen classes listBox
        self._listBox2 = wx.ListBox(self, -1, style=wx.LB_EXTENDED | wx.LB_ALWAYS_SB | wx.LB_SORT, size=(320, 400))

        # Create buttons
        btnOk = wx.Button(self, wx.ID_OK, "Ok")
        btnToTheRight = wx.Button(self, ID_BTN_TO_THE_RIGHT, "=>")
        btnToTheLeft  = wx.Button(self, ID_BTN_TO_THE_LEFT,  "<=")

        # Callbacks
        self.Bind(wx.EVT_BUTTON, self._onBtnToTheRight, id=ID_BTN_TO_THE_RIGHT)
        self.Bind(wx.EVT_BUTTON, self._onBtnToTheLeft, id=ID_BTN_TO_THE_LEFT)

        # Create info label
        lblChoice = wx.StaticText(self, -1, _("Choose classes to reverse: "))

        # Create buttons sizer
        szrBtn = wx.BoxSizer(wx.VERTICAL)
        szrBtn.Add(btnToTheRight, 0, wx.EXPAND)
        szrBtn.Add(btnToTheLeft,  0, wx.EXPAND)

        # Create lists and buttons sizer
        szrLB = wx.BoxSizer(wx.HORIZONTAL)
        szrLB.Add(self._listBox1,  0, wx.EXPAND)
        szrLB.Add(szrBtn,    0, wx.EXPAND)
        szrLB.Add(self._listBox2,  0, wx.EXPAND)

        # Create sizer
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(lblChoice, 0, wx.EXPAND)
        box.Add(szrLB,     0, wx.EXPAND)
        box.Add(btnOk,     0, wx.EXPAND)
        box.Fit(self)
        self.SetAutoLayout(True)
        self.SetSizer(box)

        # Show dialog
        self.ShowModal()
        if self.GetReturnCode() == 5101:     # abort -> empty right column

            while self._listBox2.GetCount() > 0:
                data = self._listBox2.GetClientData(0)
                name = self._listBox2.GetString(0)
                self._listBox1.Append(name, data)
                self._listBox2.Delete(0)

    def getChosenClasses(self):
        """
        Return the classes chosen by the user
        """
        ret = []
        for el in range(self._listBox2.GetCount()):
            ret.append(self._listBox2.GetClientData(el))
        return ret

    # noinspection PyUnusedLocal
    def _onBtnToTheRight(self, event):
        """
        Callback for the "=>" button
        """
        lst = list(self._listBox1.GetSelections())
        lst.sort()
        lst.reverse()
        for i in lst:
            data = self._listBox1.GetClientData(i)
            name = self._listBox1.GetString(i)
            self._listBox2.Append(name, data)
            self._listBox1.Delete(i)

    # noinspection PyUnusedLocal
    def _onBtnToTheLeft(self, event):
        """
        Callback for the "<=" button
        """
        lst = list(self._listBox2.GetSelections())
        lst.sort()
        lst.reverse()
        for i in lst:
            data = self._listBox2.GetClientData(i)
            name = self._listBox2.GetString(i)
            self._listBox1.Append(name, data)
            self._listBox2.Delete(i)


def askWhichClassesToReverse(lstClasses):
    """
    Ask which classes must be reversed

    @return list of classes
    @param list lstClasses : list of classes potentially reversible

    """
    # Ask which classes to reverse
    dlg = DlgAskWhichClassesToReverse(lstClasses)
    lstClassesChosen = dlg.getChosenClasses()
    dlg.Destroy()

    return lstClassesChosen


class IoPython(PyutIoPlugin):
    """
    Python code generation/reverse engineering

    """
    def __init__(self, oglObjects, umlFrame):

        super().__init__(oglObjects=oglObjects, umlFrame=umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        """
        return "Python code generation/reverse engineering"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        """
        return "C.Dutoit <dutoitc@hotmail.com> AND L.Burgbacher <lb@alawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        """
        return "1.0"

    def getInputFormat(self):
        """
        Return a specification tuple.
            name of the input format
            extension of the input format
            textual description of the plugin input format

        @return tuple
        """
        return "Python file", "py", "Python file format"

    def getOutputFormat(self):
        """
        Return a specification tuple.
            name of the output format
            extension of the output format
            textual description of the plugin output format

        @return tuple
        """
        return "Python file", "py", "Python file format"

    def setExportOptions(self) -> bool:
        return True

    def getVisibilityPythonCode(self, visibility: PyutVisibilityEnum):
        """
        Return the python code for a given enum value which represents the visibility

        @return String

        """
        # Note : Tested
        vis = visibility
        if vis == PyutVisibilityEnum.PUBLIC:
            code = ''
        elif vis == PyutVisibilityEnum.PROTECTED:
            code = '_'
        elif vis == PyutVisibilityEnum.PRIVATE:
            code = '__'
        else:
            self.logger.error(f"IoPython: Field code not supported : {vis}")
            code = ''
        # print " = " + str(code)
        self.logger.debug(f"Python code: {code}, for {visibility}")
        return code

    def getFieldPythonCode(self, aField: PyutField):
        """
        Return the python code for a given field

        @return String
        """
        # Initialize with class relation
        fieldCode = "self."

        fieldCode += self.getVisibilityPythonCode(aField.getVisibility())
        # Add name
        fieldCode += str(aField.getName()) + " = "

        # Add default value
        value = aField.getDefaultValue()
        if value == '':
            fieldCode += 'None'  # TODO : deduct this from type
        else:
            fieldCode += str(value)

        # Add type
        fieldCode += '\t\t\t\t\t#' + str(aField.getType()) + '\n'

        return fieldCode

    def indentStr(self, aStr):
        """
        Indent one string by one unit

        @return string
        """
        # TODO : ask which kind of indentation to be added
        return '    ' + str(aStr)

    def indent(self, lstIn):
        """
        Indent every lines of the lstIn by one unit

        @return list
        """
        lstOut = []
        for el in lstIn:
            lstOut.append(self.indentStr(str(el)))
        return lstOut

    def getOneMethodCode(self, aMethod: PyutMethod, writePass: bool = True) -> List[str]:
        """
        Return the python code for a given method

        @param aMethod : ..
        @param writePass : Write "pass" in the code ?

        @return list of strings

        """
        methodCode: List[str] = []
        currentCode = "def "

        # Add visibility
        currentCode += self.getVisibilityPythonCode(aMethod.getVisibility())
        # Add name
        currentCode += str(aMethod.getName()) + "(self"

        # Add parameters (parameter, parameter, parameter, ...)
        # TODO : add default value ?
        params = aMethod.getParams()
        if len(params) > 0:
            currentCode += ", "
        for i in range(len(params)):
            # Add param code
            paramCode = ""
            paramCode += params[i].getName()
            if params[i].getDefaultValue() is not None:
                paramCode += "=" + params[i].getDefaultValue()
            if i < len(aMethod.getParams())-1:
                paramCode += ", "
            if (len(currentCode) % 80) + len(paramCode) > MaxWidth:  # Width limit
                currentCode += "\n" + self.indentStr(self.indentStr(paramCode))
            else:
                currentCode += paramCode

        # End first(s) line(s)
        currentCode += "):\n"

        # Add to the method code
        methodCode.append(currentCode)
        # currentCode = ""

        # Add comments
        methodCode.append(self.indentStr('"""\n'))
        methodCode.append(self.indentStr('(TODO : add description)\n\n'))

        # Add parameters
        params = aMethod.getParams()
        # if len(params)>0: currentCode+=", "
        for i in range(len(params)):
            methodCode.append(self.indentStr('@param ' + str(params[i].getType()) + ' ' + params[i].getName() + '\n'))

        # Add others
        if aMethod.getReturns() is not None and len(str(aMethod.getReturns())) > 0:
            methodCode.append(self.indentStr('@return ' + str(aMethod.getReturns()) + '\n'))
        methodCode.append(self.indentStr('@since 1.0' + '\n'))
        methodCode.append(self.indentStr('@author ' + '\n'))
        methodCode.append(self.indentStr('"""\n'))
        if writePass:
            methodCode.append(self.indentStr('pass\n'))

        # Return the field code
        return methodCode

    def getMethodsDicCode(self, aClass):
        """
        Return a dictionary of method code for a given class

        @return dictionary of String, keys are methods names
        """
        clsMethods = {}
        for aMethod in aClass.getMethods():
            # Separation
            txt = "\n\n" + self.indentStr("#>---------------------------------"  "---------------------------------------\n")
            lstCodeMethod = [txt]

            # Get code
            subcode = self.getOneMethodCode(aMethod)

            # Indent and add to main code
            # for el in self.indent(subcode):
            # lstCodeMethod.append(str(el))
            lstCodeMethod += self.indent(subcode)

            clsMethods[aMethod.getName()] = lstCodeMethod

        # Add fields
        if len(aClass.getFields()) > 0:
            # Create method __init__ if it does not exist
            if '__init__' not in clsMethods:
                # Separation
                lstCodeMethod = ["\n\n    #>-------------------------------" + "-----------------------------------------\n"]

                # Get code
                subcode = self.getOneMethodCode(PyutMethod('__init__'), False)

                # Indent and add to main code
                for el in self.indent(subcode):
                    lstCodeMethod.append(str(el))
                # for el in subcode:
                # lstCodeMethod.append('    ' + str(el))
                # lstCodeMethod.append("\n\n")
                clsMethods['__init__'] = lstCodeMethod

            # Add fields
            clsInit = clsMethods['__init__']
            for aField in aClass.getFields():
                clsInit.append(self.indentStr(self.indentStr(self.getFieldPythonCode(aField))))
        return clsMethods

    def write(self, oglObjects):
        """
        Data saving
        @param oglObjects : list of exported objects

        """
        # Ask the user which destination file he wants
        directory = self._askForDirectoryExport()
        if directory == "":
            return False

        # Init
        self.logger.info("IoPython Saving...")
        classes = {}

        # Add top code
        TopCode = ["#!/usr/bin/env python\n", "__version__ = '$"+"Revision: 1.0 $'\n",
                   "__author__ = ''\n",
                   "__date__ = ''\n",
                   "\n\n"
                   ]

        # Create classes code for each object
        for el in [oglObject for oglObject in oglObjects if isinstance(oglObject, OglClass)]:
            # Add class definition
            aClass = el.getPyutObject()     # TODO
            txt = "class " + str(aClass.getName())        # Add class name
            fathers = aClass.getParents()
            if len(fathers) > 0:                          # Add fathers
                txt = txt + "("
                for i in range(len(fathers)):
                    txt = txt + fathers[i].getName()
                    if i < len(fathers)-1:
                        txt = txt + ", "
                txt = txt + ")"
            txt = txt + ":\n"
            codeClass = [txt]

            # Get methods
            clsMethods = self.getMethodsDicCode(aClass)

            # Add __init__ Method
            if '__init__' in clsMethods:
                methodCode = clsMethods['__init__']
                codeClass += methodCode
                del clsMethods['__init__']

            # Add others methods in order
            for aMethod in aClass.getMethods():
                methodName = aMethod.getName()

                try:
                    methodCode = clsMethods[methodName]
                    codeClass += methodCode
                except (ValueError, Exception) as e:
                    print(f'{e}')

            # Save to classes dictionary
            codeClass.append("\n\n")
            classes[aClass.getName()] = codeClass

        # Add classes code
        # print directory
        # print os.sep
        for (className, classCode) in list(classes.items()):
            filename = directory + os.sep + str(className) + ".py"
            file = open(filename, "w")
            file.writelines(TopCode)
            file.writelines(classCode)
            file.close()

        self.logger.info("IoPython done !")

        wx.MessageBox(_("Done !"), _("Python code generation"), style=wx.CENTRE | wx.OK | wx.ICON_INFORMATION)

    def getPyutClass(self, orgClass, filename="", pyutclass=None):
        """
        Return a PyutClass made from the python class object orgClass.
        If a pyutclass is given, it is modified in place.

        @param orgClass
        @param string filename : filename of the class
        @param PyutClass pyutclass : pyutclass to modify
        @return PyutClass
        @since 1.0
        """
        import types
        from inspect import getfullargspec

        # Verify that parameters types are acceptable
        if type(orgClass) not in [type, type]:
            self.logger.error(f"IoPython/getPyutClass: Wrong parameter for orgClass:")
            self.logger.error(f"IoPython Expected ClassType or TypeType, found {type(orgClass)}")
            return None

        # create objects
        cl = orgClass
        if pyutclass is None:
            pc = PyutClass(cl.__name__)       # A new PyutClass
        else:
            pc = pyutclass
        pc.setFilename(filename)          # store the class' filename
        methods = []                      # List of methods for this class

        # Extract methods from the class
        # clmethods = [me for me in list(cl.__dict__.values()) if type(me) == types.FunctionType]
        clmethods = [me for me in list(cl.__dict__.values()) if isinstance(me, types.FunctionType)]

        # Add the methods to the class
        for me in clmethods:
            # Remove visibility characters
            if me.__name__[-2:] != "__":
                if me.__name__[0:2] == "__":
                    func_name = me.__name__[2:]
                elif me.__name__[0] == "_":
                    func_name = me.__name__[1:]
                else:
                    func_name = me.__name__
            else:
                func_name = me.__name__
            meth = PyutMethod(func_name)     # A new PyutMethod

            # Add the method's params
            args = getfullargspec(me)
            if args[3] is None:
                firstDefVal = len(args[0])
            else:
                firstDefVal = len(args[0]) - len(args[3])
            for arg, i in zip(args[0], list(range(len(args[0])))):
                # don't add self, it's implied
                # defVal = None
                if arg != "self":
                    if i >= firstDefVal:
                        defVal = args[3][i - firstDefVal]
                        if type(defVal) == bytes:
                            defVal = '"' + defVal + '"'
                        param = PyutParam(arg, "", str(defVal))
                    else:
                        param = PyutParam(arg)
                    meth.addParam(param)
            methods.append(meth)

            # Set the visibility according to naming conventions
            if me.__name__[-2:] != "__":
                if me.__name__[0:2] == "__":
                    meth.setVisibility(PyutVisibilityEnum.PRIVATE)
                elif me.__name__[0] == "_":
                    meth.setVisibility(PyutVisibilityEnum.PROTECTED)
        # methods.sort(lambda x, y: cmp(x.getName(), y.getName()))
        pc.setMethods(methods)

        fields = None
        try:
            fe: FieldExtractor = FieldExtractor(pc.getFilename())
            fields = fe.getFields(pc.getName())
            # fields = FieldExtractor(pc.getFilename()).getFields(pc.getName())
        except IOError:
            import sys
            import os
            self.logger.error(f"File {pc.getFilename()} not found in actual dir")
            self.logger.error(f"actual dir is {os.getcwd()}")
            for path in sys.path:
                try:
                    fields = FieldExtractor(
                        path + os.sep + pc.getFilename()).getFields(
                        pc.getName())
                    break
                except IOError:
                    self.logger.error(f"Not found either in {path}{os.sep}{pc.getFilename()}")
                    pass
        if fields is None:
            self.logger.info(f"Could not extract from file {pc.getFilename()}")
        fds = []
        if fields:
            for name, init in list(fields.items()):
                if init == "":
                    init = None
                vis: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
                if len(name) > 1:
                    if name [-2:] != "__":
                        if name[0:2] == "__":
                            vis: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
                            name = name[2:]
                        elif name[0] == "_":
                            vis: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
                            name = name[1:]
                fds.append(PyutField(name, "", init, vis))

        # fds.sort(lambda x, y: cmp(x.getName(), y.getName()))
        pc.setFields(fds)
        return pc

    def reversePython(self, umlFrame, orgClasses, files):
        """
        Reverse engineering
        Classes come from self introspection !!!
        """

        # get a list of classes info for classes in the display list
        # classes = [res[name] for name in res.keys() if name in display]
        classes = [cl for cl in orgClasses
                   if ((type(cl) == type) or
                       (type(cl) == type))]

        self.logger.info(f'classes: {classes}')

        # Add extension class; TODO : find a better way to do that
        for cl in orgClasses:
            try:
                if str(type(cl)).index("class") > 0:
                    if cl not in classes:
                        classes.append(cl)
            except (ValueError, Exception) as e:
                print(f'{e}')

        objs = {}  # Dictionary classname/OglClass
        # create the PyutClass objects for each class
        for cl in classes:
            try:
                # create objects
                pc = self.getPyutClass(cl, files[cl])
                po = OglClass(pc)                 # A new OglClass
                umlFrame.addShape(po, 0, 0)
                po.autoResize()
                objs[cl.__name__] = po
            except (ValueError, Exception) as e:
                print(f"Error while creating class of type {cl},  {e}")

        # now, search for paternity links
        for po in list(objs.values()):
            pc = po.getPyutObject()     # TODO
            # skip object, it has no parent
            if pc.getName() == "object":
                continue
            currentClass = None
            for el in orgClasses:
                if el.__name__ == pc.getName():
                    currentClass = el
                    break
            if currentClass is None:
                print("Reverse error 527")
                continue

            try:
                fatherClasses = [cl for cl in classes if cl.__name__ in [x.__name__ for x in currentClass.__bases__]]
            except (ValueError, Exception) as e:
                fatherClasses = []
                print(f'{e}')

            fatherNames = [item.__name__ for item in fatherClasses]
            for father in fatherNames:
                dest = objs.get(father)
                if dest is not None:  # maybe we don't have the father loaded
                    umlFrame.createInheritanceLink(po, dest)

        # def cmpHeight(a, b):
        #     xa, ya = a.GetSize()
        #     xb, yb = b.GetSize()
        #     return cmp(yb, ya)

        # Sort by descending height
        objs = list(objs.values())
        # objs.sort(cmpHeight)
        objs.sort()

        # Organize by vertical descending sizes
        x = 20
        y = 20
        # incX = 0
        incY = 0
        for po in objs:
            incX, sy = po.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, sy)
            # find good coordinates
            if x + incX >= umlFrame.maxWidth:
                x = 20
                y += incY
                incY = sy
            po.SetPosition(x, y)
            x += incX

    def read(self, oglObjects, umlFrame):
        """
        reverse engineering

        @param oglObjects : list of imported objects
        @param umlFrame : Pyut's UmlFrame
        """
        # Ask the user which destination file he wants
        # directory=self._askForDirectoryImport()
        # if directory=="":
        #    return False
        (lstFiles, directory) = self._askForFileImport(True)
        if len(lstFiles) == 0:
            return False

        # Add to sys.path
        sysPath.insert(0, directory+os.sep)

        print("Directory = " + directory)
        umlFrame.setCodePath(directory)
        lstModules = []
        files = {}
        for filename in lstFiles:
            file = os.path.splitext(filename)[0]
            print("file=", file)

            try:
                module = __import__(file)
                importlib.reload(module)
                lstModules.append(module)
            except (ValueError, Exception) as e:
                print(f"Error while trying to import file {file}, {e}")

        # Get classes
        classesDic = {}
        for module in lstModules:
            for cl in list(module.__dict__.values()):
                if type(cl) in (type, type):
                    classesDic[cl] = 1
                    modname = cl.__module__.replace(".", os.sep) + ".py"
                    files[cl] = modname
        classes = list(classesDic.keys())

        # Remove wx.Python classes ? TODO
        classes = askWhichClassesToReverse(classes)
        if len(classes) == 0:
            return

        try:
            wx.BeginBusyCursor()
            self.reversePython(umlFrame, classes, files)
        except (ValueError, Exception) as e:
            print(f"Error while reversing python file(s)! {e}")
        wx.EndBusyCursor()
