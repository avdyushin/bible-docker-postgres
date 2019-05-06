#!/usr/bin/python

import fileinput

for line in fileinput.input():
    if not line.startswith('('):
        continue
    l = line.replace('(', '').split(',')
    new, old = int(l[0]), int(l[1])
    if new == old:
        continue
    s = "sed -i -e 's/^({},/x({},/g' rst_bible_verses.sql".format(old, new)
    print(s)
