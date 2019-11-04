

class PyutScripting(object):
    def __init__(self, mainFrame):
        self._mainFrame = mainFrame
        self._params = []

    def setParams(self, params):
        self._params = params

    def openFile(self, filename):
        self._mainFrame.loadByFilename(filename)

    def getPlugins(self):
        return self._mainFrame.plugMgr.getOutputPlugins()

    def exportToPS(self, filename):
        self._mainFrame.printDiagramToPostscript(filename)
