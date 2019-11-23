
from logging import Logger
from logging import getLogger


class PyutXmlFinder:
    """
    Chunks of code in the plugins that are littered all over the place
    """
    clsLogger: Logger = None

    def __init__(self):

        PyutXmlFinder.clsLogger = getLogger(__name__)
