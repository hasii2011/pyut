
from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue

from org.pyut.history.commands.DeleteOglLinkedObjectCommand import DeleteOglLinkedObjectCommand

from org.pyut.general.Globals import cmp

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum


class BaseOglClassCommand(DeleteOglLinkedObjectCommand):

    def __init__(self, shape=None):
        """

        Args:
            shape: The shape to serialize/deserialize
        """
        super().__init__(shape)

    def serialize(self) -> str:
        """
        Serialize an OglClass

        Returns:  A string representation of the data needed by the command.
        """
        # serialize the data common to all OglObjects
        serialShape = DeleteOglLinkedObjectCommand.serialize(self)

        pyutClass: PyutClass = self._shape.pyutObject
        classDescription = pyutClass.description

        if pyutClass.getStereotype() is not None:
            classStereotypeName = pyutClass.getStereotype().name
        else:
            classStereotypeName = ""

        classShowStereotype = repr(pyutClass.getShowStereotype())
        classShowMethods = repr(pyutClass.showMethods)
        classShowFields = repr(pyutClass.showFields)

        fields = []
        for field in pyutClass.fields:
            fieldName = field.name
            fieldType = field.type.__str__()
            fieldDefaultValue = field.defaultValue
            fieldVisibility = field.visibility.__str__()
            fields.append((fieldName, fieldType, fieldDefaultValue, fieldVisibility))

        methods = []
        for method in pyutClass.methods:
            methodName = method.name
            methodVisibility = method.getVisibility().__str__()
            methodReturns = method.returnType.__str__()

            params = []
            for param in method.parameters:
                paramName = param.name
                paramType = param.type.__str__()
                paramDefaultValue = param.defaultValue
                params.append((paramName, paramType, paramDefaultValue))

            modifiers = []
            for modifier in method.modifiers:
                modifierName = modifier.name
                modifiers.append(modifierName)

            methodProfile = (methodName, methodVisibility,
                             methodReturns, repr(params),
                             repr(modifiers))

            methods.append(methodProfile)

        serialShape += tokenizeValue("classDescription", classDescription)
        serialShape += tokenizeValue("classStereotypeName", classStereotypeName)
        serialShape += tokenizeValue("classShowStereotype", classShowStereotype)
        serialShape += tokenizeValue("classShowMethods", classShowMethods)
        serialShape += tokenizeValue("classShowFields", classShowFields)
        serialShape += tokenizeValue("fields", repr(fields))
        serialShape += tokenizeValue("methods", repr(methods))

        return serialShape

    def deserialize(self, serializedData):
        """
        Deserialize the data needed by the deleted OglCass

        Args:
            serializedData: serialized data needed by the command.
        """
        from pyutmodel.PyutMethod import PyutMethod
        from pyutmodel.PyutParameter import PyutParameter
        from pyutmodel.PyutField import PyutField

        from pyutmodel.PyutStereotype import PyutStereotype
        from pyutmodel.PyutModifier import PyutModifier

        # deserialize the data common to all OglObjects
        DeleteOglLinkedObjectCommand.deserialize(self, serializedData)

        # deserialize properties of the OglClass (first level)
        classDescription    = deTokenize("classDescription", serializedData)
        classStereotypeName = deTokenize("classStereotypeName", serializedData)
        classShowStereotype = eval(deTokenize("classShowStereotype", serializedData))
        classShowMethods    = eval(deTokenize("classShowMethods", serializedData))
        classShowFields     = eval(deTokenize("classShowFields", serializedData))

        methods = eval(deTokenize("methods", serializedData))
        fields   = eval(deTokenize("fields", serializedData))

        # set up the first level properties of the pyutClass
        pyutClass: PyutClass = self._shape.pyutObject
        pyutClass.description = classDescription

        if cmp(classStereotypeName, ""):
            pyutStereo = PyutStereotype(classStereotypeName)
            pyutClass.setStereotype(pyutStereo)

        pyutClass.setShowStereotype(classShowStereotype)
        pyutClass.showMethods = classShowMethods
        pyutClass.showFields  = classShowFields

        for field in fields:

            fieldName = field[0]
            fieldType = field[1]
            fieldDefaultValue = field[2]
            fieldVisibility = field[3]
            pyutClass.addField(PyutField(fieldName,
                                         fieldType,
                                         fieldDefaultValue,
                                         fieldVisibility))

        methodsList = []
        # deserialize methods of the pyutClass
        for methodProfile in methods:

            # construction of a method
            methodName:       str                = methodProfile[0]
            methodVisibility: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(methodProfile[1])
            methodReturns:    PyutType           = PyutType(value=methodProfile[2])

            method = PyutMethod(name=methodName, visibility=methodVisibility, returnType=methodReturns)

            # deserialize method's params so we get a tuple (name, Type, defaultValue)
            params = eval(methodProfile[3])
            for param in params:
                paramName = param[0]

                # construction of the type of the param
                paramType = param[1]
                # pyutType = PyutType(paramType)   Not used
                paramDefaultValue = param[2]

                # creates and add the param to the method
                method.addParameter(PyutParameter(paramName, paramType, paramDefaultValue))

            # deserialize method's modifiers, so we get a list of names
            # that we have to transform into a list of PyutModifiers.
            modifiersNames = eval(methodProfile[4])
            modifiers: PyutModifiers = PyutModifiers([])
            for modifierName in modifiersNames:
                modifiers.append(PyutModifier(modifierName))

            # add the modifiers to the method
            method.setModifiers(modifiers)
            # add the method to the list of methods
            methodsList.append(method)

        # add all the methods to the list
        pyutClass.methods = methodsList
