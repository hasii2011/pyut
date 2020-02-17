
import wx

from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin
from org.pyut.model.PyutClass import PyutClass
from org.pyut.ogl.OglClass import OglClass
from org.pyut.PyutMethod import PyutMethod


class IoJavascript(PyutIoPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.3 $
    """

    def getName(self) -> str:
        """
        This method returns the name of the plugin.

        @return string
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        return "Javascript reverse engineering"

    def getAuthor(self) -> str:
        """
        This method returns the author of the plugin.

        @return string
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        return "C.Dutoit <dutoitc@hotmail.com>"

    def getVersion(self) -> str:
        """
        This method returns the version of the plugin.

        @return string
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        return "1.0"

    def getInputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        # return None if this plugin can't read.
        # otherwise, return a tupple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return "Javascript file", "js", "Javascript file format"

    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tuple
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """

        return None

    def read(self, oglObjects, umlFrame):
        """
        reverse engineering

        """
        (lstFiles, directory) = self._askForFileImport(True)
        if len(lstFiles) == 0:
            return False

        if 1:
            wx.BeginBusyCursor()

            # Read all files
            for filename in lstFiles:
                f = open(filename)
                datas = f.read()
                f.close()
                jsr = JSReader(datas)
                jsr.process()
                functions = jsr.getFunctions()
                print(("import JS: ", len(functions), " functions found"))

                # Add objects
                self._addObjects(functions, umlFrame)

        wx.EndBusyCursor()

    def _addObjects(self, functions, umlFrame):
        """
        Add objects to PyUt UMLFrame
        functions is list of function
        function is dictionnary of ('functionName', 'parameters', 'javadoc')
        """
        # Create classes
        classes = {}        # key=classname; value = (function, [functions])
        for f1 in functions:
            for f2 in functions:
                # f2 is f1 + "_" + f2 ? -> class member
                if f2["functionName"].upper().startswith(
                        f1["functionName"].upper() + "_"):
                    classes[f1["functionName"]] = (f1, [])
                    break

        # Add class members
        for classname in list(classes.keys()):
            for f in functions:
                if f["functionName"].upper().startswith(classname.upper() + "_"):
                    f["functionName"] = f["functionName"][len(classname)+1:]
                    classes[classname][1].append(f)

        # create objects
        for classname in list(classes.keys()):
            classFunction = classes[classname][0]
            classParameters = classFunction["parameters"]
            classJavadoc = classFunction["javadoc"]

            # Create class
            pc = PyutClass(classname)        # A new PyutClass
            po = OglClass(pc)                 # A new OglClass
            pc.setDescription(classJavadoc[0] + "\r\n" + classJavadoc[1])

            # Add method constructor
            methods = pc.getMethods()
            method = PyutMethod(classname)
            params = method.getParams()
            params.append(classParameters)
            method.setParams(params)
            methods.append(method)

            # Add methods
            for function in classes[classname][1]:
                functionName = function["functionName"]
                parameters = function["parameters"]
                method = PyutMethod(functionName)
                params = method.getParams()
                params.append(parameters)
                method.setParams(params)
                methods.append(method)
            pc.setMethods(methods)

            # Refresh
            umlFrame.addShape(po, 0, 0)
            po.autoResize()


class JSReader:

    def __init__(self, datas):
        """
        Constructor
        @param datas string Javascript source
        """
        self._datas = datas
        self._pos = 0
        self._functions = []

    def getFunctions(self):
        """
        Return list of functions; function is declared as explicit dictionnary
        """
        return self._functions

    def process(self):
        """
        Process parsing
        """
        lastJavadoc = None
        # while self._pos < len(self._datas) and self._pos > -1:
        while len(self._datas) > self._pos > -1:

            self._readBlanks()
            if self._datas[self._pos:self._pos+3] == "/**":
                ret = self._readJavadocCommentsBlock()
                # print "JAVADOC: "
                # print "    title  =", ret[0]
                # for el in ret[2]:
                    # print "    javadoc= ", el
                # for el in ret[1].split("\n"):
                    # print "    text   =  ", el
                lastJavadoc = ret
            elif self._datas[self._pos:self._pos+2] == "//":
                self._skipLine()
            elif self._datas[self._pos:self._pos+8] == "function":
                ret = self._readFunction()
                # print "FUNCTION: "
                # print "    name       = ", ret[0]
                # print "    parameters = ", ret[1]
                self._functions.append({"functionName": ret[0],
                                        "parameters": ret[1],
                                        "javadoc": lastJavadoc
                                        })
                lastJavadoc = None
            elif self._datas[self._pos:self._pos+3] == "var":
                self._skipLine()
            else:
                # print "before=", self._datas[self._pos-9:self._pos]
                # print "after=", self._datas[self._pos:self._pos+9]
                # break
                self._skipLine()
            # print "pos=", self._pos

    def _skipLine(self):
        """
        Read until end of line and skip result
        """
        self._pos = self._datas.find("\n", self._pos)+1
        if self._pos == 0:
            self._pos = -1

    def _readBlanks(self):
        """
        Read blanks
        exit when self._datas[self._pos] is not blank (or line return)
        """
        while self._pos < len(self._datas) and self._datas[self._pos] in [' ', '\n', '\r', '\t']:
            self._pos += 1

    def _readJavadocCommentsBlock(self):
        """
        Read something like /**...*/
        @return [title, comments, javadoc list]
        javadoc list is [(tag, value, comments)]
        """
        # Read javadoc
        pos1 = self._pos
        pos2 = self._datas.find("*/", pos1)
        self._pos = pos2+2
        javadoc = self._datas[pos1:pos2+2]

        # Read title
        pos = 0
        while javadoc[pos] in ['/', '*', ' ', '\r', '\n', '\t']:
            pos += 1
        pos2 = javadoc.find('\n', pos)
        title = javadoc[pos:pos2]
        if title[-1] == '\r':
            title = title[:-1]
        pos = pos2 + 1

        # Read others things
        comments = ""
        lstJavadoc = []
        while pos < len(javadoc):
            while pos < len(javadoc) and \
                    javadoc[pos] in ['/', '*', ' ', '\r', '\n', '\t']:
                pos += 1
            if pos >= len(javadoc):
                break

            # Read line
            pos2 = javadoc.find('\n', pos)
            if pos2 == -1:
                break
            line = javadoc[pos:pos2-1]
            if len(line) > 1 and line[-1] == '\r':
                line = line[:-1]

            # Handle line
            if len(line) > 0:
                if line[0] == "@":
                    pos = line.find(" ")
                    lstJavadoc.append((line[1:pos], line[pos+1:]))
                else:
                    comments += line + "\r\n"

            # Next
            pos = pos2+1

        # self._pos = pos
        return [title, comments, lstJavadoc]

    def _readFunction(self):
        """
        Read a function
        @return functionName
        """
        # Verifications
        if self._datas[self._pos:self._pos+8] != "function":
            raise Exception("Can't read function(1)")

        # Read function name
        pos1 = self._datas.find('(', self._pos)
        functionName = self._datas[self._pos + 9:pos1]

        # Read parameters
        pos2 = self._datas.find(')', pos1)
        parameters = self._datas[pos1+1:pos2]
        pos2 = self._datas.find("{", pos2) + 1

        # Read function
        indent = 1
        while indent > 0:
            c = self._datas[pos2]
            if c == '{':
                indent += 1
            elif c == '}':
                indent -= 1
            pos2 += 1
        self._pos = self._datas.find('\n', pos2)+1

        return functionName, parameters

    def readBlock(self, delim):
        """
        Read a block, delimited by delim1, delim2
        """
        pos = self._datas.find(delim, self._pos)
        if pos == -1:
            raise Exception(f"No end delimitor for {delim}")
        txt = self._datas[self._pos:pos+1]
        self._pos = pos
        return txt
