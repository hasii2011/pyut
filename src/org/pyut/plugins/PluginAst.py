

from ast import NodeVisitor
from ast import AnnAssign
from ast import Name
from ast import NameConstant
from ast import Subscript
from ast import List
from ast import Dict
from ast import ClassDef


class Visitor(NodeVisitor):

    def __init__(self, className):

        self._className = className
        # compiler.visitor.ASTVisitor.__init__(self)
        super().__init__()
        self._result = {}

    def getResult(self):
        return self._result

    def visit_ClassDef(self, node: ClassDef):
        if node.name == self._className:
            for child in node.body:
                self.visit(child)

    def visitAssTuple(self, node):
        retList = []
        for child in node.nodes:
            retList.append(self.visit(child))
        return retList

    def visitAssAttr(self, node):
        return self.visit(node.expr) + "." + node.attrname

    def visit_AnnAssign(self, node: AnnAssign):
        strRep: str = node.__str__()
        print(f'strRep: {strRep}')
        target: Name = node.target
        if isinstance(node.annotation, Subscript):
            annotation: Subscript  = node.annotation
            val:   Name       = annotation.value
            declaration:  str        = f'{target.id}: {val.id}'
            self._result[declaration] = ''
            return
        else:
            annotation:  Name = node.annotation
            declaration:   str  = f'{target.value.id}: {annotation.id}'

        nc:     NameConstant = node.value
        if annotation.id == 'int' or annotation.id == 'float':
            self._result[declaration] = str(nc.n)
        elif annotation.id == 'str':
            self._result[declaration] = str(nc.s)
        else:
            self._result[declaration] = str(nc.value)

    def visit_Assign(self, node):
        targets = []
        for n in node.targets:
            targets.append(n.id)

        if isinstance(node.value, List):
            val: List = node.value.elts
            valStr: str = str(val)
        elif isinstance(node.value, Dict):
            valStr: str = '{}'
        else:
            valStr: str = "what!!"

        declaration:   str = f'{targets[0]}'
        self._result[declaration] = valStr
        #  return

        expr = self.visit(val)
        if expr is None:
            print(node.expr)
        target = targets[-1]
        if isinstance(expr, list):  # expr is a list
            for i, j in zip(target, expr):
                if isinstance(i, type("")) and i[0:5] == "self.":
                    if j is not None and isinstance(j, type("")):
                        if i[5:] not in self._result:
                            self._result[i[5:]] = j
                    else:
                        if i[5:] not in self._result:
                            self._result[i[5:]] = ""
        else:  # expr is not a list
            if isinstance(target, type("")) and target[0:5] == "self.":
                if expr is not None:
                    if target[5:] not in self._result:
                        self._result[target[5:]] = expr
                else:
                    if target[5:] not in self._result:
                        self._result[target[5:]] = ""
        for i in range(len(targets[:-1])):
            if isinstance(targets[i], type("")) and targets[i][0:5] == "self.":
                if targets[i][5:] not in self._result:
                    self._result[targets[i][5:]] = targets[i+1]

    def visitConst(self, node):
        return str(node.value)

    def visitUnarySub(self, node):
        return "-" + str(self.visit(node.expr))

    def visit_Name(self, node: Name):
        return node.id

    def visitTuple(self, node):
        retList = []
        for n in node.nodes:
            retList.append(self.visit(n))
        return retList

    def visitGetattr(self, node):
        return str(self.visit(node.expr)) + "." + str(node.attrname)
