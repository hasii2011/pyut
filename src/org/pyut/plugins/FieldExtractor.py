
import re


class FieldExtractor(object):
    def __init__(self, filename):
        self._filename = filename

    def getFields(self, className):
        def removePart(string, char):
            i = string.find(char)
            if i != -1:
                return string[:i]
            return string
        regvar = re.compile(r"^\s*self\.(.*)=(.*)")
        regclass = re.compile(r"^\s*class\s+" + className.strip())
        regnextclass = re.compile(r"^\s*class\s+")
        regmultiline = re.compile(r"\\s*$")
        lines = open(self._filename).readlines()
        found = {}
        inClass = 0
        buffer = ""
        multiline = 0
        for line in lines:
            # skip other classes in the same file
            # TODO : beware, this will interrupt if there's an inner class !!!
            if not inClass:
                if regclass.search(line):
                    inClass = 1
                else:
                    continue
            else:
                if regnextclass.search(line):
                    break
            if multiline:
                line = buffer + line.strip()
            if regmultiline.search(line):
                buffer = line[:line.rindex("\\")]
                print("buffer", buffer)
                multiline = 1
                continue
            else:
                multiline = 0
            res = regvar.findall(line)
            if res:
                for name, init in res:
                    name = removePart(name, ".")
                    name = removePart(name, "(")
                    name = removePart(name, "[")
                    name = removePart(name, "+")
                    name = removePart(name, "-")
                    name = removePart(name, "*")
                    name = removePart(name, "/")
                    name = removePart(name, "%")
                    init = removePart(init, "#")
                    name = name.strip()
                    if name not in found:
                        found[name] = init.strip()
                        print("adding", repr(name.strip()), init.strip())
        return found

# def main():
#     import sys
#     if len(sys.argv) > 1:
#         res = FieldExtractor(sys.argv[1]).getFields(sys.argv[2])
#         for name, init in res.items():
#             print name, "=", init
#
# if __name__ == "__main__":
#     main()
