
# import compiler # TODO need a replacement for this

from ast import NodeVisitor
from ast import PyCF_ONLY_AST
from ast import parse
from ast import walk


# class Visitor(compiler.visitor.ASTVisitor):


class Visitor(NodeVisitor):

    def __init__(self, className):

        self._className = className
        # compiler.visitor.ASTVisitor.__init__(self)
        super().__init__()
        self._result = {}

    def getResult(self):
        return self._result

    def visitClass(self, node):
        if node.name == self._className:
            self.visit(node.code)

    def visitAssTuple(self, node):
        retList = []
        for child in node.nodes:
            retList.append(self.visit(child))
        return retList

    def visitAssAttr(self, node):
        return self.visit(node.expr) + "." + node.attrname

    def visitAssign(self, node):
        targets = []
        for n in node.nodes:
            targets.append(self.visit(n))
        expr = self.visit(node.expr)
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

    def visitName(self, node):
        return node.name

    def visitTuple(self, node):
        retList = []
        for n in node.nodes:
            retList.append(self.visit(n))
        return retList

    def visitGetattr(self, node):
        return str(self.visit(node.expr)) + "." + str(node.attrname)

    # def visitAdd(self, node):
    #    return self.visit(node.left) + "+" + self.visit(node.right)

    # def visitFunction(self, node):
    #    print "fonction :", node.name

    # def visitCallFunc(self, node):
    #    s = self.visit(node.node) + "("
    #    for n in node.args:
    #        s += self.visit(n) + ", "
    #    s = s[:-2] + ")"
    #    return s

# compiler.walk(ast, Visitor())


class FieldExtractor(object):
    def __init__(self, filename):
        self._filename = filename

    def getFields(self, className):

        visitor = Visitor(className)
        # compiler.walk(compiler.parseFile(self._filename), visitor)
        walk(parse(self._filename, PyCF_ONLY_AST))

        return visitor.getResult()


# def main():
#     import sys
#     if len(sys.argv) > 1:
#         print(compiler.parseFile(sys.argv[1]))
#         res = FieldExtractor(sys.argv[1]).getFields(sys.argv[2])
#         print("-" * 76)
#         for name, val in list(res.items()):
#             print(name, "=", val)
#
#
# if __name__ == "__main__":
#     main()
