def newClass():
    click(Pattern("ClickNewClass.png").similar(0.10).targetOffset(-391,-22))


for x in range (6):
    newClass()

click(Pattern("OpenTree.png").targetOffset(-123,-23))

rightClick(Pattern("RightClickTarget2.png").targetOffset(-58,-73))

click(Pattern("SelectDeleteDocument2.png").targetOffset(-10,-69))

click(Pattern("1590447777283.png").targetOffset(35,-33))