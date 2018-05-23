#!/usr/bin/env python3
import punctCode

# Given a file name, loop line by line and convert the string of a Key (filename), phonetic word,
# plus the pitch accent code to a big list.
def parseToneFile(fn):
	# TODO: Handle empty/invalid lines gracefully
	print("Parsing file: \"%s\"" % fn)
	dat = [];
	for line in open(fn,'r'):
		[key,w,n]=line.split(':')
		print(" => importing \"%s\"" % key)
		pc = punctCode.parseToneString(key,w,n.strip())
		dat.append(pc)
	return dat;

# Parse the list, pucntList is now a list of objects containing grouped mora, and the individual
# mora's high/low filled/unfilled graph symbol.	
punctList = parseToneFile('tofugu_files/example_codes_tofugu.txt')

print("Saving svgs...")
# For each one, dump an SVG
for pc in punctList:
	# using default sizing. Units are in pixels.
	filename = ('tofugu_examples/%s.svg' % (pc.key));
	print(" => saving \"%s\" as \"%s\"" % (pc.key, filename))
	pc.toSVG(filename, style='font-weight:bold;',\
		padding_lr=30, padding_tb=15)


