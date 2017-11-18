#!/usr/bin/python

import sys
print(sys.argv[0])
print(type(sys.argv[1]))
print(int(sys.argv[1])+1)
output_file="outputbot_"+sys.argv[1]+".csv"
print(output_file)
