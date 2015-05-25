#!/usr/bin/python

import sys
output =  open("output.jpeg", 'wb')
for line in sys.stdin:
    output.write(bytearray(int(i, 16) for i in line.strip().split(' ')))

output.close();
