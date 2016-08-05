#!/usr/bin/env python

import os
import re
import sys

fileIn = sys.argv[1]
fileOut = sys.argv[2]

bibOut = ""
regexpBibDeb = re.compile(r"^@.+\{(.+),$")
regexpBibEnd = re.compile(r"^\}$")
with open(fileIn, 'r') as fileRead:
	fileRead = fileRead.readlines()

	curBib = False
	for line in fileRead:
		line = line.rstrip('\n')
		s = regexpBibDeb.search(line)

		if s and not curBib :
			