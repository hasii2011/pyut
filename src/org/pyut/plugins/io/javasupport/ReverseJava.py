
from typing import Dict
from typing import NewType
from typing import Set
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

Implementors = NewType('Implementors', Set[OglClass])
Extenders    = NewType('Extenders', Set[OglClass])

ReversedClasses = NewType('ReversedClasses', Dict[str, OglClass])
SubClassMap     = NewType('SubClassMap', Dict[OglClass, Extenders])
InterfaceMap    = NewType('InterfaceMap', Dict[OglClass, Implementors])

# Constants
CLASS_MODIFIER   = ["public", "protected", "private", "abstract", "final", "static", "strictfp"]
FIELD_MODIFIERS  = ["public", "protected", "private", "static", "final", "transient", "volatile"]
METHOD_MODIFIERS = ["public", "protected", "private", "abstract", "static", "final", "synchronized", "native", "strictfp"]


class ReverseJava:

    def __init__(self, umlFrame: UmlClassDiagramsFrame):

        self.logger: Logger = getLogger(__name__)

        self._classes:      ReversedClasses = ReversedClasses({})
        self._subClassMap:  SubClassMap  = SubClassMap({})
        self._interfaceMap: InterfaceMap = InterfaceMap({})

        self._umlFrame: UmlClassDiagramsFrame = umlFrame

    @property
    def reversedClasses(self) -> ReversedClasses:
        return self._classes

    @property
    def subClassMap(self) -> SubClassMap:
        return self._subClassMap

    def interfaceMap(self) -> InterfaceMap:
        return self._interfaceMap

    def parseFile(self, filename):
        """
        Creates entries accessible via the reverseClasses property.
        Superclass and subclass relationships are captured in the subClassMap property
        Interface relationships are captured in the interfaceMap property.

        Args:
            filename:  The java file to parse

        """
        # Read the file in lstFile
        f = open(filename, "r")
        lstFileTempo = f.readlines()
        f.close()
        lstFile = []
        for el in lstFileTempo:
            fraction = el.split()
            lstFile += self.__mySplit(fraction)
            lstFile.append("\n")
        # lstFileTempo = None

        # Read file
        currentPos = 0
        try:
            while currentPos < len(lstFile):
                # Analyze word
                self.__logMessage(f"\n analyzing word {currentPos}")
                self.__logMessage("***")
                self.__logMessage(f"{lstFile}")

                # Read comments
                currentPos = self._readComments(lstFile, currentPos)

                # new class ?
                if self._isClassBeginning(lstFile, currentPos):
                    currentPos = self._readClass(lstFile, currentPos)
                currentPos += 1
        except (ValueError, Exception) as e:
            self.logger.error(f'Error in ReverseJava - {type(e)} {e}')
            raise e

        # finally:
            # Best display
            # self.layoutDiagram()

    def layoutDiagram(self):
        """
        Layout out the generated OglClasses and their inheritance and interface relationships

        """

        for oglClass in list(self._classes.values()):
            self._umlFrame.addShape(oglClass, 0, 0)
            oglClass.autoResize()

        self.__logMessage('Layout subclasses map keys')
        for parent in self._subClassMap.keys():
            self.__logMessage(f'BaseClass: {parent}')
            extenders: Extenders = self._subClassMap[parent]
            for child in extenders:
                self.__logMessage(f'{parent} <--- {child}')
                self._umlFrame.createInheritanceLink(child=child, parent=parent)

        for interface in self._interfaceMap.keys():
            implementors: Implementors = self._interfaceMap[interface]
            for implementor in implementors:
                self._umlFrame.createInterfaceLink(src=implementor, dst=interface)

        self.__logMessage("Improving display")
        Margin = 10
        x = Margin
        y = Margin
        dy = 10
        for po in list(self._classes.values()):
            self.__logMessage(".")
            try:  # Catch exceptions
                (w, h) = po.GetSize()
                dy = max(dy, h + Margin)
                adjustedX: int = round(x + w / 2)
                adjustedY: int = round(y + h / 2)
                po.SetPosition(adjustedX, adjustedY)
                po.autoResize()
                x += w + Margin
                if x > 200:
                    x = Margin
                    y += dy
                    dy = Margin
            except (ValueError, Exception) as e:
                self.__logMessage(f"Error in IoJavaReverse.py {e}. Please report !")

    def _readClass(self, lstFile, currentPos):
        """
        Read a class from a list of strings, beginning on a given position.
        This class reads one class from lstFile, from currentLine.

        Args:
            lstFile:    list of instructions read from the file to analyze
            currentPos: last read line pointer, Pyut's OglClass object, class name

        Returns:  Returns the updated current position (read line pointer)
        """
        # Pass modifiers
        while lstFile[currentPos] in CLASS_MODIFIER:
            currentPos += 1

        # Read "class"
        currentPos += 1

        # Read class name
        className = lstFile[currentPos]
        self.__logMessage(f"Reading className {className}")
        currentPos += 1

        # Create a class object
        self.__addClass(className)

        # Remove end of lines
        currentPos = self.__selectNextAfter(lstFile, currentPos, ['\n', ''])

        # Read inheritance and interface parameters
        while lstFile[currentPos] in ["extends", "implements"]:
            if lstFile[currentPos] == "extends":
                # Next token, points on superClass name
                currentPos += 1

                # Get superclass
                superClass = lstFile[currentPos]
                currentPos += 1
                self.__logMessage(f' - superclass={superClass}')

                # Create a class object
                self.__addClass(superClass)
                self.__updateExtendersMap(className, superClass)

            else:  # implements
                shouldExit: bool = False
                self.__logMessage(f"Reading interface... {lstFile[currentPos:currentPos + 5]}")
                while not shouldExit:
                    # Next token, points on first interface name
                    currentPos += 1
                    currentPos = self.__selectNextAfter(lstFile, currentPos, ['\n', ''])

                    # Get interface name
                    interfaceName = lstFile[currentPos]
                    self.__logMessage(f" - interface={interfaceName}")
                    currentPos += 1

                    # Create a class object
                    self.__addClass(interfaceName)
                    self.__updateInterfaceMap(className, interfaceName)

                    # Read comments
                    currentPos = self._readComments(lstFile, currentPos)
                    currentPos = self.__selectNextAfter(lstFile, currentPos, ['\n', ''])

                    # Exit if no more implementations
                    if lstFile[currentPos] != ",":
                        shouldExit = True

            # Remove end of lines
            currentPos = self.__selectNextAfter(lstFile, currentPos, ['\n', ''])

        # Read comments
        currentPos = self._readComments(lstFile, currentPos)

        # Remove end of lines
        currentPos = self.__selectNextAfter(lstFile, currentPos, ['\n', ''])

        # End of class ?
        if lstFile[currentPos] == ";":
            return currentPos

        # Remove end of lines
        currentPos = self.__selectNextAfter(lstFile, currentPos, ['\n', ''])

        # Read comments
        currentPos = self._readComments(lstFile, currentPos)

        # Class beginning ?
        self.__logMessage("lstFile=%s" % lstFile[currentPos:currentPos + 5])
        if lstFile[currentPos] != "{":
            self.__logMessage(f"DBG class >> {lstFile[currentPos]}")
            self.__logMessage(f"Unexpected characters : {lstFile[currentPos:currentPos + 5]}")
            self.__logMessage("   exiting class reader !\n")
            return currentPos
        currentPos += 1

        # Read class
        level = 1  # level of indentation
        while level > 0 and currentPos < len(lstFile):
            # Read comments
            currentPos = self._readComments(lstFile, currentPos)

            # Change level ?
            if lstFile[currentPos] == "{":
                level += 1
            elif lstFile[currentPos] == "}":
                level -= 1
            elif level == 1:
                (succeeded, aTuple, currentPos) = self._readVariable(lstFile, currentPos, True)
                if succeeded:
                    (modifiers, fieldType, names_values) = aTuple
                    self.__addClassFields(className, modifiers, fieldType, names_values)
                else:
                    # Read comments
                    currentPos = self._readComments(lstFile, currentPos)

                    # Read method
                    (succeeded, aTuple, currentPos) = self._readMethod(lstFile, currentPos, className, True)
                    if succeeded:
                        (modifiers, methodType, name, lstFields) = aTuple
                        self.__addClassMethod(className, modifiers, methodType, name, lstFields)

            # Next token ?
            if level > 0:
                currentPos += 1
        return currentPos

    def _readComments(self, lstFile, currentPos):
        """
        Read all comments

        @param lstFile : list of instructions read from the file to analyze
        @param currentPos : current position in the list
        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.0
        """
        self.__logMessage("readComments")
        # Set comment terminator
        if lstFile[currentPos][:2] == "//":
            terminator = "\n"
        elif lstFile[currentPos][:2] == "/*":
            terminator = "*/"
        else:  # No comments => return initial position
            return currentPos

        # Pass comments
        currentPos += 1
        while lstFile[currentPos][-len(terminator):] != terminator and currentPos < len(lstFile):
            currentPos += 1
        return currentPos + 1

    def _readMethod(self, lstFile, currentPos, className, returnValues=False):
        """
        Read a method.
        Is considered as function :
        - Something of the following type :
            Method_Declaration ::= Method_Header MethodBody
            Method_Header ::= Method_Modifiers Result_Type Method_Declaration
                              Throws
            ResultType ::= Type or void
            Method_Declaration ::= identifier (Formal_Parameter_List)
            Formal_Parameter_List ::= [Formal_Parameter_List,] Formal_Parameter
            Formal_Parameter ::= final Type Variable_Declaration_Id
            Throws ::= throws Class_Type_List
            Class_Type_List ::= [Class_Type_List,] ClassType
            ...

        @param lstFile : list of instructions read from the file to analyze
        @param currentPos : current position in the list
        @param className : current class name, used to detect constructors
        @param returnValues : bool, indicate if we must return values
                              (types, ...)
        @return bool : True if a variable start at the given position
                or tuple : (bool, True if succeeded;
                            tuple : (modifiers, type, name, parameters),
                            final position)
                parameters type if list of tuple (type, name, def value)
        @Author C.Dutoit
        @since 1.0
        """
        # Init
        pos = currentPos
        lstModifiers = []

        # Debug info
        self.__logMessage("readMethod, %s..." % (lstFile[currentPos:currentPos + 5]))

        # Pass field modifiers
        while lstFile[pos] in METHOD_MODIFIERS:
            lstModifiers.append(lstFile[pos])
            pos += 1

        # Read type (only for non-constructors)
        if lstFile[pos] != className:
            returnType = lstFile[pos]
            pos += 1
        else:
            returnType = ""

        # Read method name (identifier)
        methodName = lstFile[pos]
        pos += 1

        # valid following ?
        if lstFile[pos] != "(":
            if returnValues:
                return False, None, currentPos
            else:
                return False

        # Read the parameters
        # TODO : int class(int pi=(...)); doesn't work here ! (parenthesis)
        parameters = []
        pos += 1
        self.__logMessage("*******************************")
        self.__logMessage("Reading parameters %s" % lstFile[pos:pos + 10])
        while lstFile[pos] != ")":
            # Get parameter
            paramType = lstFile[pos]
            pos += 1
            name = lstFile[pos]
            pos += 1
            self.__logMessage("type=%s, name=%s" % (type, name))

            # Read default value
            defaultValue = ""
            if lstFile[pos] == "=":
                pos += 1
                while lstFile[pos] not in [")", ","]:
                    defaultValue += lstFile[pos] + " "
                    pos += 1
                if lstFile[pos] == ",":
                    pos += 1
                self.__logMessage(f"={defaultValue}")
            if defaultValue == "":
                defaultValue = None

            # Pass \n ?
            pos = self.__selectNextAfter(lstFile, pos, ["\n"])

            # ',' => new parameter => next position
            if lstFile[pos] == ",":
                pos += 1

            # Pass \n ?
            pos = self.__selectNextAfter(lstFile, pos, ["\n"])

            # Append to parameters list
            parameters.append((paramType, name, defaultValue))
        # pos = self._readParagraph(lstFile, pos, "(", ")")
        self.__logMessage("*******************************")
        pos += 1

        # Pass \n ?
        pos = self.__selectNextAfter(lstFile, pos, ["\n"])

        # pass throws ?
        if lstFile[pos] == "throws":
            pos += 1
            while lstFile[pos][-1] not in [";", "{"]:
                pos += 1

        # End of function ?
        if lstFile[pos][-1] == ";":
            if returnValues:
                return True, (lstModifiers, returnType, methodName, parameters), pos
            else:
                return True

        # The following is not a function corps ? => return
        if lstFile[pos] != "{":
            if returnValues:
                return False, None, currentPos

        # Read function corps
        pos = self.__readParagraph(lstFile, pos, "{", "}")
        if returnValues:
            return True, (lstModifiers, returnType, methodName, parameters), pos
        else:
            return True

    def _readVariable(self, lstFile, currentPos, returnValues=False):
        """
        Test if the current position starts a variable.
        Is considered as variable :
        - Something of the following type :
           Field_Declaration    ::= Field_Modifiers Type Variable_Declaration;
           Variable_Declaration ::= [Variable_Declaration,] Variable_Declaration
           Variable_Declaration  ::= Variable_Declaration_ID
                                    [ = Variable_Initializer ]
           Variable_Initializer ::= ... etc

        @param lstFile : list of instructions read from the file to analyze
        @param currentPos : current position in the list
        @param returnValues : bool, indicate if we must return values
                              (types, ...)
        @return bool : True if a variable start at the given position
                or tuple : (bool, True if succeeded;
                            tuple : (modifiers, type, tuple: (name, values));
                            final position)
        @Author C.Dutoit
        @since 1.0
        """
        # Init
        pos = currentPos
        lstModifiers = []
        lstNames_Values = []

        # Pass field modifiers
        while lstFile[pos] in FIELD_MODIFIERS:
            lstModifiers.append(lstFile[pos])
            pos += 1

        # Read type
        theType = lstFile[pos]
        pos += 1

        # Read first variable declaration
        lstNames_Values.append((lstFile[pos], None))
        self.__logMessage(f"Adding name {lstFile[pos]}, following {lstFile[pos:pos + 2]}")
        pos += 1

        # valid following ?
        if lstFile[pos] not in [",", "=", ";"]:
            if returnValues:
                return False, None, currentPos
            else:
                return False

        # Continue reading...
        while pos < len(lstFile):
            if lstFile[pos] == ",":
                pos += 1
                # lstModifiers.append(lstFile[pos])
                lstNames_Values.append((lstFile[pos], None))
                pos += 1
            elif lstFile[pos] == ";":
                if returnValues:
                    return True, (lstModifiers, theType, lstNames_Values), pos
                else:
                    return True
            elif lstFile[pos] == "=":
                # TODO : change this; pass values
                pos += 1
                while lstFile[pos] != ";":
                    pos += 1
            else:
                if returnValues:
                    return False, None, currentPos
                else:
                    return False

            # TODO : this does not support int a=8, b=4; ('=')

        if returnValues:
            return False, None, currentPos
        else:
            return False

    def _isClassBeginning(self, lstFile, currentPos):
        """
        Return True if the specified line is a class beginning

        @param lstFile : list of instructions read from the file to analyze
        @param currentPos : current position in the list
        @return bool : True if the specified line do begin a class
        @author C.Dutoit
        @since 1.0
        """
        lstUsedCM = []  # List of used class modifiers
        # Evaluate each argument
        pos = currentPos
        while pos < len(lstFile):
            el = lstFile[pos]
            # Is current argument a class modifier ?
            if el in CLASS_MODIFIER:
                # if not modified, add it as modifiers list
                if not (el in lstUsedCM):
                    lstUsedCM.append(el)
                else:  # Already used => not a valid class beginning
                    # TODO : print warning ?
                    return False
            elif el == "class":  # class token => this is a class
                return True
            elif el == "interface":  # interface token => take it as a class
                return True
            else:  # unacceptable token => not a class beginning
                return False
            pos += 1
        return False

    def __addClass(self, className: str) -> OglClass:
        """
        Add a class to the dictionary of classes

        Args:
            className: Name of the class to be added

        Returns: OglClass instance for the class

        """
        # If the class name exists already, return the instance
        if className in self._classes:
            return self._classes[className]

        # Create the class
        pc: PyutClass = PyutClass(className)  # A new PyutClass
        po: OglClass = OglClass(pc)  # A new OglClass

        self._classes[className] = po

        return po

    def __addClassFields(self, className, modifiers, fieldType, names_values):
        """
        Add fields to a class
        Note : Default value can be None. (see names_values)

        @param String className : Name of the class to be added
        @param String modifiers : Fields modifiers
        @param String fieldType      : Fields type
        @param tuple names_values : tuple of (name, default values)

        """
        # Get class fields
        po: OglClass = self._classes[className]
        pc: PyutClass = cast(PyutClass, po.pyutObject)
        classFields = pc.fields

        # TODO fix this crazy code to use constructor and catch exception on bad input
        # Get visibility
        if "private" in modifiers:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
        elif "protected" in modifiers:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
        elif "public" in modifiers:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
        else:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        # Add all
        for (name, value) in names_values:
            classFields.append(PyutField(name, fieldType, value, visibility))

    def __addClassMethod(self, className, modifiers, returnType, name, lstFields):
        """
        Add a method to a class
        Parameters example:
        ```java
            static private int getName(int a, long b)
            - className = name of the class which own this method
            - static private => modifiers
            - int            => return type
            - getName        => name
            - int a, long b  => lstFields => ["int a", "long b"]
        ```
        Note : Default value can be None. (see names_values)

        Args:
            className:  Name of the class to add
            modifiers:  Method modifiers
            returnType: Method returnType
            name:       Method name
            lstFields:  List of string lstFields : Method fields
        """

        self.__logMessage("Adding method %s for class %s" % (name, className))
        self.__logMessage("(modifiers=%s; returnType=%s)" % (modifiers, returnType))
        # Get class fields
        po: OglClass = self._classes[className]
        pc: PyutClass = cast(PyutClass, po.pyutObject)

        # TODO fix this crazy code to use constructor and catch exception on bad input
        # Get visibility
        if "private" in modifiers:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
        elif "protected" in modifiers:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
        elif "public" in modifiers:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
        else:
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        # Add method
        methods = pc.methods

        if returnType == '\n' or returnType == '' or returnType == 'void' or returnType is None:
            pm = PyutMethod(name, visibility)
        else:
            retType: PyutType = PyutType(returnType)
            pm = PyutMethod(name, visibility, retType)

        for (paramType, name, defaultValue) in lstFields:
            param = PyutParam(name, paramType, defaultValue)
            pm.addParam(param)
        methods.append(pm)

    def __readParagraph(self, lstFile, currentPos, paragraphStart, paragraphStop):
        """
        Read a paragraph; Handle sublevels;
        Read a paragraph. A paragraph is limited by two specific tokens.
        As a paragraph can include itself a paragraph, this function
        does read sub-paragraphs.

        @param lstFile : list of instructions read from the file to analyze
        @param currentPos : current position in the list
        @param paragraphStart : token which identify the beginning of the
                                paragraph
        @param paragraphStop  : token which identify the end of the paragraph
        @return end of paragraph position
        @Author C.Dutoit
        @since 1.1.2.5
        """
        # We must begin on the paragraph start token
        if lstFile[currentPos] != paragraphStart:
            return currentPos

        # Init
        level = 1

        # Read paragraph
        while level > 0:
            currentPos += 1
            if lstFile[currentPos] == paragraphStart:
                level += 1
            elif lstFile[currentPos] == paragraphStop:
                level -= 1
        return currentPos

    def __selectNextAfter(self, lstFile, currentPos, lstElements):
        """
        Select next position after an End-Of-Line

        @param lstFile : list of instructions read from the file to analyze
        @param currentPos : current position in the list
        @param lstElements : Elements to pass
        @return Next position after EOL
        @Author C.Dutoit
        @since 1.0
        """
        while (currentPos < len(lstFile)) and (lstFile[currentPos] in lstElements):
            currentPos += 1
        return currentPos

    def __mySplit(self, lstIn):
        """
        Do more splitting on a list of String.
        Split elements like [")};"]     into    ¨[")", "}", ";"]

        or

        ["Humberto;"]   into   ["Humberto", ";"]


        Args:
            lstIn: list of String to be split

        Returns: the split list
        """
        TO_BE_SPLIT = ['{', '}', ';', ')', '(', ',']
        lstOut = []
        # Split each element
        for el in lstIn:
            pos = 0
            while len(el) > 0 and pos < len(el):
                if el[pos] in TO_BE_SPLIT:
                    if pos > 0:
                        lstOut.append(el[:pos])
                    lstOut.append(el[pos])
                    el = el[pos + 1:]
                    pos = 0
                else:
                    pos += 1

            # Add el
            if len(el) > 0:
                lstOut.append(el)

        # Return split list
        return lstOut

    def __updateExtendersMap(self, className: str, superClass: str):
        """
        Update the map of superclasses (base classes) and the classes that extend
        it (subclasses)
        Args:
            className:  The original class
            superClass: The name of the super class
        """
        oglSuperClass: OglClass = self._classes[superClass]
        oglClass:      OglClass = self._classes[className]

        if oglSuperClass in self._subClassMap:
            extenders: Extenders = self._subClassMap[oglSuperClass]
            extenders.add(oglClass)
        else:
            extenders = Extenders(set())
            extenders.add(oglClass)

        self.logger.debug(f'Make extender entry for {superClass} - subclass: {className}')
        self._subClassMap[oglSuperClass] = extenders

    def __updateInterfaceMap(self, className: str, interfaceName: str):

        interfaceClass: OglClass = self._classes[interfaceName]
        implementor:    OglClass = self._classes[className]

        if interfaceClass in self._interfaceMap:
            implementors: Implementors = self._interfaceMap[interfaceClass]
            implementors.add(implementor)
        else:
            implementors = Implementors(set())
            implementors.add(implementor)

        self.logger.debug(f'Class {className} implements {interfaceName}')
        self._interfaceMap[interfaceClass] = implementors

    def __logMessage(self, theMessage: str):
        """
        Probably not a correct implementation but that is what I got !!
        Args:
            theMessage:

        """
        self.logger.debug(f"{theMessage}")
