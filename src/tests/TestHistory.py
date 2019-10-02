#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from HistoryManager import *
from commandGroup import *
from printCommand import *
"""
@author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
This is the unit test of the HistoryManager. It was tested on 21.11.2005
and it works perfectly. It's also a good example to see how it works.
"""

#creating the history
h = HistoryManager(None)

#creating the command groups
cg1 = CommandGroup("cg1")
cg2 = CommandGroup("cg2")
cg3 = CommandGroup("cg3")
cg4 = CommandGroup("cg4")

#commands for group 1
pc1a = PrintCommand()
pc1b = PrintCommand()

#commands for group 2
pc2a = PrintCommand()
pc2b = PrintCommand()

#commands for group 3
pc3a = PrintCommand()
pc3b = PrintCommand()

#commands for group 4
pc4a = PrintCommand()
pc4b = PrintCommand()

# set the messages of the commands
pc1a.setMessage("pc1a")
pc1b.setMessage("pc1b")
pc2a.setMessage("pc2a")
pc2b.setMessage("pc2b")
pc3a.setMessage("pc3a")
pc3b.setMessage("pc3b")
pc4a.setMessage("pc4a")
pc4b.setMessage("pc4b")

#add the commands to the groups
cg1.addCommand(pc1a)
cg1.addCommand(pc1b)
cg2.addCommand(pc2a)
cg2.addCommand(pc2b)
cg3.addCommand(pc3a)
cg3.addCommand(pc3b)
cg4.addCommand(pc4a)
cg4.addCommand(pc4b)

#add the groups to the history
h.addCommandGroup(cg1)
h.addCommandGroup(cg2)
h.addCommandGroup(cg3)

#check if the undo/redo and add method works correctly
print "supposed to undo cg3 : "
h.undo()
print "supposed to undo cg2 : "
h.undo()
print "supposed to add cg4 and remove cg2 : "
h.addCommandGroup(cg4)
print "supposed to add cg3 : "
h.addCommandGroup(cg3)
print "supposed to undo cg3 : "
h.undo()
print "supposed to undo cg4 : "
h.undo()
print "supposed to undo cg1 : "
h.undo()
print "supposed to do nothing : "
h.undo()
print "-- nothing --"

print "supposed to add cg2 and delete cg1,3,4 : "
h.addCommandGroup(cg2)
print "supposed to undo cg2 : "
h.undo()
print "supposed to add cg1, cg3, cg4 and delete cg2 : "
h.addCommandGroup(cg1)
h.addCommandGroup(cg3)
h.addCommandGroup(cg4)
print "supposed to undo cg4, cg3, cg1 :"
h.undo()
h.undo()
h.undo()
print "supposed to redo cg1, cg3, cg4 :"
h.redo()
h.redo()
h.redo()
print "supposed to do nothing : "
h.redo()
print "-- nothing --"
print "supposed to add cg2"
h.addCommandGroup(cg2)
print "check that the file '" + h._fileName + "' contains groups cg1,3,4,2 and then press [enter]"
try:
    input()
finally:
    print "should be false : ", h.isRedoPossible()
    print "should be true : ", h.isUndoPossible()
    print "should be cg2 : ", h.getCommandGroupToUndo().getComment()
    h.undo()
    print "should be cg4 : ", h.getCommandGroupToUndo().getComment()
    print "should be cg2 : ", h.getCommandGroupToRedo().getComment()
    h.undo()
    print "should be cg3 : ", h.getCommandGroupToUndo().getComment()
    print "should be cg4 : ", h.getCommandGroupToRedo().getComment()
    h.undo()
    print "should be cg1 : ", h.getCommandGroupToUndo().getComment()
    print "should be cg3 : ", h.getCommandGroupToRedo().getComment()
    h.undo()
    print "should be cg1 : ", h.getCommandGroupToRedo().getComment()
    print "should be true : ", h.isRedoPossible()
    print "should be false : ", h.isUndoPossible()
    print "check that the file '" + h._fileName + "' doesn't exist anymore"
    h.destroy()
    print "!!!DON'T CARE ABOUT THE FINAL ERROR MESSAGE!!!"
