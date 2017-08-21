#!/usr/bin/env python3
import svgwrite as svgw
# if you have Python-Package (pip), install the SVG dependancy with
#    pip3 install svgwrite

####
# This script is a "simple" tool for generating pitch accent patern graphs as shown in Dogen's
# Patreon series (no affliation). 

class punctCode:
	# Unicode Hiragana Range 3041 -> 309F
	# Small Hirigana 30:41,43,45,47,49,83,85,87,8E
	# Small Ka/Ke 95,96
	# Small Tsu 63
	# Unused Hirigana (we still allow) 30:90,91
	# Unicode Katakana Range (Hirigana + 96d [0x60])
	MODIFY_SET='ゃゅょぁぃぅぇぉ';
	HIRIGANA_MIN	= 0x3041;
	HIRIGANA_MAX	= 0x309F;
	KATAKANA_OFFSET	= 0x60;
	KATAKANA_MIN	= HIRIGANA_MIN+KATAKANA_OFFSET;
	KATAKANA_MAX	= HIRIGANA_MAX+KATAKANA_OFFSET;
	# TODO: Warn users if they give me Kanji and not kana!
	
	def __init__(self, key, mora, tones):
		self.key = key
		self.mora = mora
		self.tones = tones
	def __str__(self):
		sm=''
		for m in self.mora:
			sm=sm+(',%s' % m)
		st=''
		for t in self.tones:
			st=st+(',%d' % t)
		return '<'+sm[1:]+':'+st[1:]+'>'
	def __repr__(self):
		return self.__str__()
	def isSafe(self): # report if length's match
		return len(self.mora) == len(self.tones)
	def warn(s, ind=0):
		print('=> WARNING: %s' % s)
	def toSVG(self, outputFN, \
		dx=50, dy=None, rad=7, stroke=3, circ_stroke=None, \
		color='#000000', padding=25, padding_tb=None, padding_lr=None, \
		offset=20, \
		font_family='Noto Sans', font_height=27, style=''):
		
		# Now dow the variable renaming
		# These variables control the core geometry of the image. You shouldn't ever need to change
		# this code to configure your image. Simply use the various optional named arguments in the
		# toSVG method above.
		STEP_HEIGHT	= dx
		STEP_WIDTH	= STEP_HEIGHT if dy == None else dy
		LINE_STROKE	= stroke
		CIRC_STROKE = stroke if circ_stroke == None else circ_stroke
		CIRC_RAD	= rad
		PADDING_TB	= padding_tb if (padding_tb != None) else padding
		PADDING_LR	= padding_lr if (padding_lr != None) else padding
		TEXT_OFFSET	= offset
		TEXT_HEIGHT	= font_height
		COLOR		= color

		# SVG image placement to move us off of the origin.
		MOVE_DOWN	= PADDING_TB + STEP_HEIGHT;
		MOVE_RIGHT	= PADDING_LR;
		# never no when you'll need 1/sqrt(2) (0.707). Much more critical than pi.
		ISQRT2		= (2**-0.5)

		# Generate width and height for SVG. Generally the max function used here won't do anything
		# as the two arguments are the same, but if we screw up this makes sure we can see the full
		# result even in it's deranged form.
		WIDTH		= 2*PADDING_LR + STEP_WIDTH*(max(len(self.tones),len(self.mora))-1);
		HEIGHT		= 2*PADDING_TB + STEP_HEIGHT + TEXT_OFFSET + TEXT_HEIGHT;

		# Generate drawing workspace
		dwg = svgw.Drawing(filename=outputFN, size=(WIDTH, HEIGHT))
		# put everything in a group
		master = dwg.add(dwg.g(id='master_group'))
		# use the group to fix the origin placement
		master.translate(MOVE_RIGHT, MOVE_DOWN)
		# put the graph points and lines in one group
		graph = master.add(dwg.g(id='graph'))
		# loop throug each mora point
		for iT,T in enumerate(self.tones):
			# location is one of two set heights, and a step to the right for each word.
			loc = (iT*STEP_WIDTH,-(T%2)*STEP_HEIGHT)
			# only mora that we've coded get filled circles. There are workarounds if you want
			# everything or odd characters to be filled though.
			currentFill = COLOR if (T & 0b10) == 0 else 'none'
			# and put in that damn circle.
			graph.add(dwg.circle(center=loc, r=CIRC_RAD, \
				stroke=COLOR, stroke_width=CIRC_STROKE, fill=currentFill))

			if not (T & 0b100): # don't bother adding the connection line if bit 3 is set
				# Draw a line between the current and previous point
				startPoint = loc;
				endPoint = pT['loc'];
				if (loc[1] == pT['loc'][1]): # remove radus from each endPoint
					startPoint = (startPoint[0] - CIRC_RAD, startPoint[1])
					endPoint = (endPoint[0] + CIRC_RAD, endPoint[1])
				else: # remove diagonal length
					startPoint = (startPoint[0] - CIRC_RAD*ISQRT2, startPoint[1])
					endPoint = (endPoint[0] + CIRC_RAD*ISQRT2, endPoint[1])
					if (pT['loc'][1] > loc[1]):
						startPoint	= (startPoint[0], startPoint[1]	+ CIRC_RAD*ISQRT2)
						endPoint	= (endPoint[0], endPoint[1]		- CIRC_RAD*ISQRT2)
					else:
						startPoint	= (startPoint[0], startPoint[1]	- CIRC_RAD*ISQRT2)
						endPoint	= (endPoint[0], endPoint[1]		+ CIRC_RAD*ISQRT2)
				graph.add(dwg.line(start=startPoint, end=endPoint, \
					stroke_width=LINE_STROKE, stroke=COLOR))
			pT = {'iT':iT, 'T':T, 'loc':loc} # save the previous location so we can compute up/down

		# now draw each mora (note: きゅ is one not two, while けっ is two not one.)
		# by setting the font size here and the text anchor position we fix the alignment to be the
		# center of the circles in the graph above
		moras = master.add(dwg.g(id='moras',\
			font_size=TEXT_HEIGHT,\
			text_anchor='middle',\
			fill=COLOR,
			font_family=font_family))
		for iM,M in enumerate(self.mora):
			# each section
			text = moras.add(dwg.text(M, insert=(iM*STEP_WIDTH, TEXT_OFFSET+TEXT_HEIGHT), id='moras'))
			text.attribs['style']=('text-align:center;'+style)
		# then try to save the file.
		# !!! No error handling. I wrote it in an afternoon, this isn't production code.
		# TODO: Add error handling.
		dwg.save()

# This was supposed to be a class method, but my knowledge of python isn't that strong. It worked
# until I moved the class to it's own file. So now it's just a function in the same file. I think?
# TODO: Make sure I'm implementing a class method properly.

###
# The way this method works is it takes in a key (whatever you want) as a file name, a "word"
# meaning specifically the phonetic characters to describe the word (katakana or hiragana), and
# a code representing the pitch accent pattern and line connection preferences for the word.
#
# The code takes the form of comma seperated groups of downstep location followed by the mora length
# of the word. For example 勉強=べんきょう would be coded as 0/4. 案内=あんない would be 3/4. A phrase
# like 涙を拭く=なみだをふく would be 1/3,0/2 Note that the を is implicitly contained in the prior 
# word. If you wanted to code 涙拭く without the を, you would need to mark the final symbol as being
# dropped by using a star. So the code for なみだふく is 1/3*,0/2. If you want to include
# the final mora following the word even without providing a symbol, set the includeFinalSymbol 
# named argument in this function to True. This allows for odaka words to include a drop without
# a specific kana being inserted.
#
# Finally, if you wanted to drop the connecting line for some reason, then put a star prior to the
# downstep location. For example, I pulled the thumbnail from Dogen's 25th video with a split 
# between べんきょう and して. To code this split use 0/4*,*0/2. This codes two heiban words, the
# first without a spot for the implied particle (as indicated by a trailing star), and a second word
# lacking a connection to the prior word (as indicated by a leading star).
def parseToneString(name,word,codes, includeFinalOpen=False):
	moraList=[];
	# First break up the word by characters
	for indLetter,letter in enumerate(word):
		primaryInsert = True;
		codepoint = ord(letter);
		# Then check for small characters in either Kana range
		if (codepoint <= punctCode.KATAKANA_MAX and codepoint >= punctCode.KATAKANA_MIN):
			codepoint = codepoint - punctCode.KATAKANA_OFFSET;
		for modify in punctCode.MODIFY_SET:
			if (codepoint == ord(modify)):
				primaryInsert = False
				break;
		
		# TODO: Check for Kanji, punctuation, etc, and handle gracefully
		
		# If the character is a "primary" character (i.e. a big Mora or a small っ)
		# Then we will insert it directly.
		if (primaryInsert or len(moraList) == 0):
			moraList.append(letter);
		# Otherwise we try to lump the special character with the previous character.
		# The exception being if we started a word with it (why the hell would we do that anyway?)
		else:
			prevLetter = moraList.pop()
			moraList.append(prevLetter+letter)
		
		# Merge small mora into individual mora
		# exempting the small　'っ'
	### At this point moraList contains the word split by mora groups
	
	### Now to assign high/low and filled data directly
	# So the code is designed to corespond to the number pattern used in the Apple Dictionary and
	# 三省堂スーパー大辞林. The first number indicates the downstep location followed by a slash
	# telling this dumb parser where the end of the word is. We will insert a symbol for each mora
	# specified by this code, with one EXTRA dot following the word representing the downstep
	# location if a particle is attached. We ASSUME the next character is a particle, unless
	# incidated otherwise. So a code of 1/2,1/2 would assume that we have 5 or 6 mora. 2 for the
	# first wird, a particle, two for the second word, and an optional ending partile. If none is
	# provided we truncate the drawing unless the downstep would occor on the non-provided particle.
	# TODO: Provide a way to omit downstep in compound entries
	
	# The way we re-encode this information is with a 4 state (2-bit) code:
	# 	00	lo filled
	#	01	hi filled
	#	10	lo empty
	#	11	hi empty
	#  a leading 3rd bit is used to indicate skipped connecting lines
	
	n=codes.split(',')
	n_code=[];
	for iCodeEntry,codeEntry in enumerate(n):
		# TODO: Handle special codes for odd corner cases
		# now split by slash
		ceSplit = codeEntry.split('/');
		dontDrawLine = 0b100 if (ceSplit[0][0] == '*' or iCodeEntry == 0) else 0;
		includeParticle = not (ceSplit[1][-1] == '*'); # draw the particle unless we say skip it
		downStep = int(ceSplit[0] if (ceSplit[0][0] != '*') else ceSplit[0][1:])
		wordLength = int(ceSplit[1] if (includeParticle) else ceSplit[1][:-1]);
		if (downStep == 0):
			n_code.append(0b00 + dontDrawLine)
			for x in range(wordLength-1):
				n_code.append(0b01)
			if (includeParticle):
				n_code.append(0b11)
		else:
			if (downStep != 1):
				n_code.append(0b00 + dontDrawLine)
			else:
				n_code.append(0b01 + dontDrawLine)

			for x in range(downStep-1):
				n_code.append(0b01)
			for x in range(wordLength-downStep):
				n_code.append(0b00)
			if (includeParticle):
				n_code.append(0b10)
	
	# we can get a mismatch if we have a word with a hanging accent point for a particle
	# that doesn't exist. If that's the case, then we will truncate the tone by default,
	# otherwise we can force the insertion of a filler symbol. If the final point is NOT for
	# an unused particle, we simply generate a mismatched graph, and warn the user. The mismatch
	# in this case should be from a problem with the input strings.
	if (len(moraList) == len(n_code)-1):
		if (includeFinalOpen):
			moraList.append('○')
		elif ((not includeFinalOpen) and (n_code[-1] & 0b10) != 0):
			n_code.pop()
	
	pc = punctCode(name, moraList, n_code)
	if (not pc.isSafe()):
		punctCode.warn('Count mismatch for \'%s\' (mora: %d, code: %d)' % \
			(name, len(pc.mora), len(pc.tones)))
	return pc

