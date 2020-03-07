
from typing import cast
from typing import Dict
from typing import NewType

from logging import Logger
from logging import getLogger

from org.pyut.experimental.GraphicalHandler import GraphicalHandler
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam

from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.PluginAst import FieldExtractor
from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

OBJECT_MAP_TYPE = NewType('OBJECT_MAP_TYPE', Dict[str, OglClass])


class ReverseEngineerPython:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def reversePython(self, umlFrame: UmlClassDiagramsFrame, classesToReverseEngineer, files):
        """
        Reverse engineering
        Classes come from introspection !!!
        """

        # get a list of classes info for classes in the display list
        # classes = [res[name] for name in res.keys() if name in display]
        classes = [cl for cl in classesToReverseEngineer if (type(cl) == type)]

        self.logger.info(f'classes: {classes}')

        # Add extension class; TODO : find a better way to do that
        for cl in classesToReverseEngineer:
            try:
                if str(type(cl)).index("class") > 0:
                    if cl not in classes:
                        classes.append(cl)
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')

        objectMap: OBJECT_MAP_TYPE = cast(OBJECT_MAP_TYPE, {})  # Dictionary className/OglClass
        # create the PyutClass objects for each class
        for cl in classes:
            try:
                # create objects
                pc = self.getPyutClass(cl, files[cl])
                po = OglClass(pc)                 # A new OglClass
                umlFrame.addShape(po, 0, 0)
                po.autoResize()
                objectMap[cl.__name__] = po
            except (ValueError, Exception) as e:
                self.logger.error(f"Error while creating class of type {cl},  {e}")

        # now, search for paternity links
        for po in list(objectMap.values()):
            pc = po.getPyutObject()     # TODO
            # skip object, it has no parent
            if pc.getName() == "object":
                continue
            currentClass = None
            for el in classesToReverseEngineer:
                if el.__name__ == pc.getName():
                    currentClass = el
                    break
            if currentClass is None:
                self.logger.error("Reverse engineer error 527")
                continue

            try:
                fatherClasses = [cl for cl in classes if cl.__name__ in [x.__name__ for x in currentClass.__bases__]]
            except (ValueError, Exception) as e:
                fatherClasses = []
                self.logger.error(f'{e}')

            fatherNames = [item.__name__ for item in fatherClasses]
            for father in fatherNames:
                dest = objectMap.get(father)
                if dest is not None:  # maybe we don't have the parent loaded
                    # umlFrame.createInheritanceLink(po, dest)
                    graphicalHandler: GraphicalHandler = GraphicalHandler(umlFrame=umlFrame, maxWidth=umlFrame.maxWidth,
                                                                          historyManager=umlFrame.getHistory())
                    graphicalHandler.createInheritanceLink(child=po, parent=dest)
        # Sort by descending height
        objectList = list(objectMap.values())
        # objectList.sort()   TODO OglClasses need a magic method for comparing

        # Organize by vertical descending sizes
        x = 20
        y = 20
        # incX = 0
        incY = 0
        for po in objectList:
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

    def getPyutClass(self, oglClass, filename: str = "", pyutClass=None):
        """
        If a pyutClass is input, it is modified in place.

        Args:
            oglClass:
            filename:   filename of the class
            pyutClass:  pyutClass to modify

        Returns:
            A PyutClass constructed from the Python class object OglClass.
        """
        import types
        from inspect import getfullargspec

        # Verify that parameters types are acceptable
        if type(oglClass) not in [type]:
            self.logger.error(f"IoPython/getPyutClass: Wrong parameter for oglClass:")
            self.logger.error(f"IoPython Expected class type, found {type(oglClass)}")
            return None

        # create objects
        cl = oglClass
        if pyutClass is None:
            pc = PyutClass(cl.__name__)       # A new PyutClass
        else:
            pc = pyutClass
        pc.setFilename(filename)          # store the class' filename
        methods = []                      # List of methods for this class

        # Extract methods from the class
        klassMethods = [me for me in list(cl.__dict__.values()) if isinstance(me, types.FunctionType)]

        # Add the methods to the class
        for me in klassMethods:
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
            pyutMethod: PyutMethod = PyutMethod(func_name)     # A new PyutMethod

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
                    pyutMethod.addParam(param)
            methods.append(pyutMethod)

            # Set the visibility according to naming conventions
            if me.__name__[-2:] != "__":
                if me.__name__[0:2] == "__":
                    pyutMethod.setVisibility(PyutVisibilityEnum.PRIVATE)
                elif me.__name__[0] == "_":
                    pyutMethod.setVisibility(PyutVisibilityEnum.PROTECTED)
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
