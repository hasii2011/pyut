#----------------------------------------------------------------------
# This file was generated by img2py.py
#

# import cPickle
import _pickle as cPickle

import zlib
import wx


def getData():
    return cPickle.loads(zlib.decompress(
'x\xda\x95\x8d\xb1\n\xc30\x0cD\xf7|\xc5A\x07w2\xf1\xd0\xe09\x01\xaf\x1a\xbch\
\r\x19kP\xfe\x7f\xaa%\x92\xe2@\x8b\x89\xe4\xe5=\xce\xbag\xd9\xc3\x90]\x98P\
\xdf\x0b\xc1\rkv\x1e\x1b\xe6\xb2no#Tz,\xa3\xae\xb1(\xc7Q\xd7\x98ON\xd1\x98\
\x94SL\xcb\xc1\x80o\x068%\xb3@\xea0\xb7\x12\xea\x00\xb4\xf2\xe7w\xfaN+\xebI\
\x10\xe4*\xff$5L\xd2M\xdek\x17\xbb\xdaMZ=\xe1~\xbb\xff\x00\xda\xf3`\xb7' ))


def getBitmap():
    return getImage().ConvertToBitmap()


def getImage():
    return wx.Image("img/class.bmp", wx.BITMAP_TYPE_ANY)

