
from org.pyut.history.HistoryUtils import getTokenValue

from DelOglLinkedObjectCommand import DelOglLinkedObjectCommand
from org.pyut.history.HistoryUtils import makeValuatedToken

from globals import cmp


class DelOglClassCommand(DelOglLinkedObjectCommand):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    It execute/undo/redo the deletion of an OglClass
    """

    def __init__(self, shape=None):
        """
        Constructor.
        @param shape    : object that is destroyed
        """
        super().__init__(shape)

    def serialize(self):
        """
        Serialize the data needed by the destroyed OglLinkedObject.
        @return a string representation of the data needed by the command.
        """
        # serialize the data common to all OglObjects
        serialShape = DelOglLinkedObjectCommand.serialize(self)

        pyutClass = self._shape.getPyutObject()
        classDescription = pyutClass.getDescription()

        if pyutClass.getStereotype() is not None:
            classStereotypeName = pyutClass.getStereotype().getName()
        else:
            classStereotypeName = ""

        classShowStereotype = repr(pyutClass.getShowStereotype())
        classShowMethods = repr(pyutClass.getShowMethods())
        classShowFields = repr(pyutClass.getShowFields())

        fields = []
        for field in pyutClass.getFields():
            fieldName = field.getName()
            fieldType = field.getType().__str__()
            fieldDefaultValue = field.getDefaultValue()
            fieldVisibility = field.getVisibility().__str__()
            fields.append((fieldName, fieldType, fieldDefaultValue, fieldVisibility))

        methods = []
        for method in pyutClass.getMethods():
            methodName = method.getName()
            methodVisibility = method.getVisibility().__str__()
            methodReturns = method.getReturns().__str__()

            params = []
            for param in method.getParams():
                paramName = param.getName()
                paramType = param.getType().__str__()
                paramDefaultValue = param.getDefaultValue()
                params.append((paramName, paramType, paramDefaultValue))

            modifiers = []
            for modifier in method.getModifiers():
                modifierName = modifier.getName()
                modifiers.append(modifierName)

            methodProfile = (methodName, methodVisibility,
                             methodReturns, repr(params),
                             repr(modifiers))

            methods.append(methodProfile)

        serialShape += makeValuatedToken("classDescription",    classDescription)
        serialShape += makeValuatedToken("classStereotypeName", classStereotypeName)
        serialShape += makeValuatedToken("classShowStereotype", classShowStereotype)
        serialShape += makeValuatedToken("classShowMethods",    classShowMethods)
        serialShape += makeValuatedToken("classShowFields",     classShowFields)
        serialShape += makeValuatedToken("fields", repr(fields))
        serialShape += makeValuatedToken("methods", repr(methods))

        return serialShape

    def unserialize(self, serializedInfos):
        """
        unserialize the data needed by the destroyed OglLinkedObject.
        @param serializedInfos   :   serialized data needed by the command.
        """
        from PyutMethod import PyutMethod
        from PyutParam import PyutParam
        from PyutField import PyutField
        from PyutType import PyutType
        from PyutStereotype import PyutStereotype
        from PyutModifier import PyutModifier

        # unserialize the data common to all OglObjects
        DelOglLinkedObjectCommand.unserialize(self, serializedInfos)

        # unserialize properities of the OglClass (first level)
        classDescription    = getTokenValue("classDescription", serializedInfos)
        classStereotypeName = getTokenValue("classStereotypeName", serializedInfos)
        classShowStereotype = eval(getTokenValue("classShowStereotype", serializedInfos))
        classShowMethods    = eval(getTokenValue("classShowMethods", serializedInfos))
        classShowFields     = eval(getTokenValue("classShowFields", serializedInfos))

        methods = eval(getTokenValue("methods", serializedInfos))
        fields   = eval(getTokenValue("fields", serializedInfos))

        # set up the first level properities of the pyutClass
        pyutClass = self._shape.getPyutObject()
        pyutClass.setDescription(classDescription)

        if cmp(classStereotypeName, ""):
            pyutStereo = PyutStereotype(classStereotypeName)
            pyutClass.setStereotype(pyutStereo)

        pyutClass.setShowStereotype(classShowStereotype)
        pyutClass.setShowMethods(classShowMethods)
        pyutClass.setShowFields(classShowFields)

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
        # unserialise methods of the pyutClass
        for methodProfile in methods:

            # construction of a method
            methodName = methodProfile[0]
            methodVisibility = methodProfile[1]
            methodReturns = methodProfile[2]
            method = PyutMethod(methodName, methodVisibility, methodReturns)

            # unserialize method's params so we get a tuple (name, Type, defaultValue)
            params = eval(methodProfile[3])
            for param in params:
                paramName = param[0]

                # construction of the type of the param
                paramType = param[1]
                pyutType = PyutType(paramType)
                paramDefaultValue = param[2]

                # creates and add the param to the method
                method.addParam(PyutParam(paramName, paramType, paramDefaultValue))

            # unserialize method's modifiers so we get a list of names
            # that whe have to transform into a list of PyutModifiers.
            modifiersNames = eval(methodProfile[4])
            modifiers = []
            for modifierName in modifiersNames:
                modifiers.append(PyutModifier(modifierName))

            # add the modifiers to the method
            method.setModifiers(modifiers)
            # add the method to the list of methods
            methodsList.append(method)

        # add all the methods to the list
        pyutClass.setMethods(methodsList)
