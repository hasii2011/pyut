#!/usr/bin/env python

__version__ = "$Revision: 1.1.1.1 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2001-11-14"

class Foo:
    """
    Short description of the class (1 line max) ended by a dot.
    Mandatory complete description of the class:
        - what it's for
        - how it works
        - sample use case

    reStructuredText samples:
        - *Important* thing, or **vital** thing.
        - `className` or `methodName` or `paramName`

    Example of code::
        truc.bidule()
        machin.chose()

    :version: $Revision: 1.1.1.1 $
    :author: Laurent Burgbacher
    :contact: lb@alawa.ch
    """
    def __init__(self):
        """
        Constructor.

        @since 1.0
        @author <email>
        """
        pass

    #>------------------------------------------------------------------------

    def method(self, param1, param2):
        """
        Short description, this method does...
        Long description if needed.

        @param type name : Description
        @param type name : Description
        @return type : What does it return
        @since 1.0
        @author <email>
        """
        # comments begin with a sharp sign (#) and last until the end of the
        # line.
        #
        # the @since take the version number in which the method first appears.
        # The actual version number is in the __version__ variable, at the
        # beginning of the file. So, the version you will put is one more than
        # the actual.
        # ex : __version__ = "$ ID 1.3$"
        # Create a new method, put it @since 1.4
        pass

    #>------------------------------------------------------------------------
    
    def calcAverage(self, numbers):
        """
        Compute the average of the given numbers.

        @param numbers[] numbers : List of numbers to average
        @return number : Average of the given numbers
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return reduce(lambda x, y: x + y, numbers) / len(numbers)
