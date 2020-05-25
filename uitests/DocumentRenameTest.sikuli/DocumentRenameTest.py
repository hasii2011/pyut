def newClass():
    click(Pattern("ClickNewClass.png").similar(0.10).targetOffset(-391,-22))
def doRename(newName):
    type(Key.LEFT,Key.CMD + Key.SHIFT)
    type(newName)
    type(Key.TAB)
    type(Key.ENTER) 

for x in range (6):
    newClass()
click(Pattern("OpenTree.png").targetOffset(-123,-23))
rightClick(Pattern("RightClickTarget0.png").targetOffset(-59,-113))
click(Pattern("SelectRenameDocument0.png").targetOffset(19,-72))
type('0')
type(Key.TAB)
type(Key.ENTER)

rightClick(Pattern("RightClickTarget1.png").targetOffset(-60,-93))
click(Pattern("SelectRenameDocument1.png").targetOffset(11,-66))
click(Pattern("DoubleClickDialogToSelect.png").targetOffset(10,0))
doRename('1')

rightClick(Pattern("RightClickTarget2.png").targetOffset(-58,-73))
click(Pattern("SelectRenameDocument2.png").targetOffset(-11,-88))
click(Pattern("DoubleClickDialogToSelect.png").targetOffset(19,0))
doRename('2')

rightClick(Pattern("RightClickTarget3.png").targetOffset(-61,-53))
click(Pattern("SelectRenameDocument3.png").targetOffset(-14,-65))
click(Pattern("DoubleClickDialogToSelect.png").targetOffset(19,0))
doRename('3')

rightClick(Pattern("RightClickTarget4.png").targetOffset(-58,-35))
click(Pattern("SelectRenameDocument4.png").targetOffset(12,-51))
click(Pattern("DoubleClickDialogToSelect.png").targetOffset(19,0))
doRename('4')

rightClick(Pattern("RightClickTarget5.png").targetOffset(-42,-15))
click(Pattern("SelectRenameDocument5.png").similar(0.77).targetOffset(27,-28))
click(Pattern("DoubleClickDialogToSelect.png").targetOffset(19,0))
doRename('5')
