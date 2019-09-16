import zlib

s = zlib.decompress(open("demo1.put").read())
pos = 0

while pos >- 1:
    pos = s.find("showFields", pos+1)
    if pos>-1: print(s[pos:pos+15])
