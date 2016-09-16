#!/usr/bin/env python

import os
import re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--completeBib', help = "Complete bibtex", type = str, default = None, nargs = '+')
parser.add_argument('-e', '--excludeFiles', help = "Exclude some files", default = False, action = "store_true")
args = parser.parse_args()

regexpBibDeb = re.compile(r"^@.+\{(.+),$")

hashBibManuscript = {}
fileBibManuscript = "./Manuscript/bib/thesis.bib"
with open(fileBibManuscript, 'r') as fileRead :
	fileRead = fileRead.readlines()

	curCitation = None
	citationKey = None
	for line in fileRead :
		s = regexpBibDeb.search(line)

		if s:
			if curCitation != None :
				if citationKey in hashBibManuscript.keys() :
					print("Error ! " + citationKey + " appears two times in " + fileBibManuscript)
				else :
					hashBibManuscript[citationKey] = curCitation
				curCitation = None
				citationKey = None

			citationKey = s.group(1)
			curCitation = line
		else :
			if curCitation != None :
				curCitation += line

	if curCitation != None :
		if citationKey in hashBibManuscript.keys() :
			print("Error ! " + citationKey + " appears two times in " + fileBibManuscript)
		else :
			hashBibManuscript[citationKey] = curCitation


newHashBibManuscript = dict(hashBibManuscript)

hashBib = {}
if args.completeBib != None :
	for bibFile in args.completeBib :
		with open(bibFile, 'r') as fileRead :
			fileRead = fileRead.readlines()

			curCitation = None
			citationKey = None
			for line in fileRead :
				s = regexpBibDeb.search(line)

				if s:
					if curCitation != None :
						if citationKey in hashBib.keys() :
							print("Error ! " + citationKey + " appears two times in " + bibFile)
						else :
							hashBib[citationKey] = curCitation
						curCitation = None
						citationKey = None

					citationKey = s.group(1)
					curCitation = line
				else :
					if curCitation != None :
						curCitation += line

			if curCitation != None :
				if citationKey in hashBib.keys() :
					print("Error ! " + citationKey + " appears two times in " + bibFile)
				else :
					hashBib[citationKey] = curCitation

listExcludeFiles = list()
if args.excludeFiles :
	FILE_EXCLUDE = "./exclude.txt"

	with open(FILE_EXCLUDE, 'r') as fileRead :
		fileRead = fileRead.readlines()

		for line in fileRead :
			fileExclude = line.rstrip('\n').replace(" ", "")
			if os.path.splittext(fileExclude)[1] == ".tex" :
				listExcludeFiles.append(fileExclude)

	print("Excluding...")
	for file in listExcludeFiles :
		print("\t" + file)


srcDir = "./Manuscript/src"

regexCite = re.compile(r"\\parencite\{([^\}]*)\}")
listSrcFiles = [os.path.join(srcDir, file) for file in os.listdir(srcDir) if os.path.splitext(file)[1] == ".tex" and (not args.excludeFiles or (file not in listExcludeFiles))]

listAlert = list()
listSrcCitations = {}
for file in listSrcFiles :
	print("----- Reading " + file + "... -----")
	with open(file, 'r') as fileRead :
		fileRead = fileRead.readlines()

		for line in fileRead :
			f = regexCite.finditer(line)

			if f != None :
				for match in f :
					citations = match.group(1)
					citations = citations.split(',')

					if len(citations) > 0 :
						for citation in citations :
							citation = citation.replace(" ", "")

							if citation not in listSrcCitations.keys() :
								listSrcCitations[citation] = True

							if citation not in hashBibManuscript.keys() :
								print("\tAlert ! Citation key " + citation + " not in " + fileBibManuscript)

								if args.completeBib != None :
									if citation not in newHashBibManuscript.keys() :
										if citation not in hashBib.keys() :
											print("\t\t--- ALERT ! Citation key " + citation + " not in bib completion !")
											listAlert.append(citation + " - " + os.path.basename(file))
										else :
											newHashBibManuscript[citation] = hashBib[citation]

if args.completeBib != None :
	bibOut = "./Manuscript/bib/thesis.bib.new"

	if os.path.isfile(bibOut) :
		os.remove(bibOut)

	with open(bibOut, 'w') as fileWrite :
		print("WRITING NEW BIB FILE")
		sortCitations = sorted(newHashBibManuscript.keys())

		cpt = 0
		while cpt < len(sortCitations) :
			if sortCitations[cpt] in listSrcCitations.keys() :
				fileWrite.write(newHashBibManuscript[sortCitations[cpt]])
			
			cpt += 1

		print("Number of citations = " + str(len(sortCitations)))


		print("Please check : ")

		# Removing duplicates
		listAlert = list(set(listAlert))

		# Ordering list
		listAlert.sort()
		for citation in listAlert :
			print("\t" + citation)
			