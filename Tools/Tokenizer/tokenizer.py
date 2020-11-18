#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

# The script will attempt to tokenize all files in the input directory
# and output a file of the same name to the output directory,
# with one token per line and with empty lines as sentence boundaries.

# arguments:
# input directory
# output directory

import os, sys
import nltk.data
from nltk.tokenize import word_tokenize
import re

abbreviationsToContract = re.compile(
		(
			'(?:'
			'(?:a\\.\\s+a\\.\\s+o)|'
			'(?:a\\.\\s+d)|'
			'(?:a\\.\\s+e)|'
			'(?:a\\.\\s+m)|'
			'(?:b\\.\\s+a)|'
			'(?:b\\.\\s+sc)|'
			'(?:co\\.\\s+ltd)|'
			'(?:d\\.\\s+h)|'
			'(?:d\\.\\s+i)|'
			'(?:dr\\.\\s+iur)|'
			'(?:e\\.\\s+t\\.\\s+a)|'
			'(?:e\\.\\s+u)|'
			'(?:e\\.\\s+v)|'
			'(?:g\\.\\s+m\\.\\s+b\\.\\s+h)|'
			'(?:i\\.\\s+d\\.\\s+r)|'
			'(?:i\\.\\s+r)|'
			'(?:i\\.\\s+s\\.\\s+d)|'
			'(?:i\\.\\s+s\\.\\s+v)|'
			'(?:i\\.\\s+v\\.\\s+m)|'
			'(?:k\\.\\s+a)|'
			'(?:k\\.\\s+k)|'
			'(?:k\\.\\s+u\\.\\s+k)|'
			'(?:m\\.\\s+a)|'
			'(?:m\\.\\s+e)|'
			'(?:m\\.\\s+sc)|'
			'(?:n\\.\\s+a)|'
			'(?:n\\.\\s+chr)|'
			'(?:o\\.\\s+a)|'
			'(?:o\\.\\s+g)|'
			'(?:o\\.\\s+\U000000E4)|'
			'(?:p\\.\\s+a)|'
			'(?:p\\.\\s+p)|'
			'(?:p\\.\\s+s)|'
			'(?:ph\\.\\s+d)|'
			'(?:rer\\.\\s+medic)|'
			'(?:rer\\.\\s+nat)|'
			'(?:rer\\.\\s+pol)|'
			'(?:rer\\.\\s+soc)|'
			'(?:s\\.\\s+a\\.\\s+e)|'
			'(?:s\\.\\s+a\\.\\s+s)|'
			'(?:s\\.\\s+m\\.\\s+s)|'
			'(?:s\\.\\s+o)|'
			'(?:s\\.\\s+p\\.\\s+a)|'
			'(?:s\\.\\s+r\\.\\s+l)|'
			'(?:s\\.\\s+r\\.\\s+o)|'
			'(?:s\\.\\s+s)|'
			'(?:s\\.\\s+u)|'
			'(?:u\\.\\s+a)|'
			'(?:u\\.\\s+a\\.\\s+m)|'
			'(?:u\\.\\s+co)|'
			'(?:u\\.\\s+dergl)|'
			'(?:u\\.\\s+dgl)|'
			'(?:u\\.\\s+s)|'
			'(?:u\\.\\s+s\\.\\s+f)|'
			'(?:u\\.\\s+s\\.\\s+w)|'
			'(?:u\\.\\s+u)|'
			'(?:u\\.\\s+v\\.\\s+m)|'
			'(?:u\\.\\s+\U000000E4)|'
			'(?:v\\.\\s+a)|'
			'(?:v\\.\\s+chr)|'
			'(?:v\\.\\s+l)|'
			'(?:v\\.\\s+l\\.\\s+n\\.\\s+r)|'
			'(?:v\\.\\s+r)|'
			'(?:z\\.\\s+b)|'
			'(?:z\\.\\s+d)|'
			'(?:z\\.\\s+t)|'
			'(?:zit\\.\\s+n)'
			')\\.'
		), re.IGNORECASE
	)
spacesToDelete = re.compile('\\s+')

controlChars = re.compile('[\u0000-\u0008\u000E-\u001F\u007F\u0080-\u009F]')

doubleQuotes = re.compile('[\u00AB\u00BB\u201C-\u201F]')
doubleQuotesReplacement = '"'

singleQuotesOpen = re.compile('(?<!\\S)[\u2039\u203A\u2018-\u201B´`](?!\\s)')
singleQuotesOpenReplacement = '\u0060'
singleQuotesClose = re.compile('(?<!\\s)[\u2039\u203A\u2018-\u201B´`]')
singleQuotesCloseReplacement = '\''
apostrophes = re.compile('(?<!\\s)[\u2039\u203A\u2019´`](?!\\s)')
apostrophesReplacement = '\''

ellipses = re.compile('[\u2026]')
ellipsesReplacement = '...'

nonHyphenDashs = re.compile('[\u2012-\u2014]|(?:-?--)|(?:[\u2011](?=\\s))')
nonHyphenDashsReplacement = '-'

def replaceSpaces(match):
	return spacesToDelete.sub('', match.group())

def contractAbbreviations(text):
	return abbreviationsToContract.sub(replaceSpaces, text)

def preTokenizeTransform(text):
	text = controlChars.sub('', text)
	text = contractAbbreviations(text)
	text = doubleQuotes.sub(doubleQuotesReplacement, text)
	text = apostrophes.sub(apostrophesReplacement, text)
	text = singleQuotesClose.sub(singleQuotesCloseReplacement, text)
	text = singleQuotesOpen.sub(singleQuotesOpenReplacement, text)
	text = ellipses.sub(ellipsesReplacement, text)
	text = nonHyphenDashs.sub(nonHyphenDashsReplacement, text)
	return text

def tokenizeParagraph(sentTokenizer, paragraph, output):
	if len(paragraph) == 0:
		return
	paragraph = preTokenizeTransform('\n'.join(paragraph))
	sentences = sentTokenizer.tokenize(paragraph)
	for sentence in sentences:
		words = word_tokenize(sentence, language='german', preserve_line=True)
		for word in words:
			output.write(word)
			output.write('\n')
		output.write('\n')

abbreviations = [
	'a', 'a.a.o', 'a.d', 'a.e', 'a.m', 'abb', 'abt', 'ae', 'ahd', 'akk',
	'al', 'anm', 'arch', 'art', 'ass', 'aufl', 'b.a', 'b.sc', 'berufl',
	'bsp', 'bspw', 'bzgl', 'bzw', 'ca', 'ch', 'chem', 'co', 'co.ltd', 'd',
	'd.h', 'd.i', 'dat', 'dipl', 'doz', 'dr', 'dr.iur', 'dt', 'e.t.a',
	'e.u', 'e.v', 'ebd', 'ec', 'einschl', 'engl', 'erg', 'etc', 'etw',
	'evtl', 'ew', 'f', 'ff', 'fl', 'fr', 'g.m.b.h', 'geb', 'gem', 'gen',
	'gg', 'ggf', 'ggfs', 'gr', 'habil', 'hg', 'hist', 'hl', 'hr', 'hrsg',
	'i', 'i.d.r', 'i.r', 'i.s.d', 'i.s.v', 'i.v.m', 'ii', 'iii', 'ing',
	'inkl', 'insb', 'intrans', 'ital', 'iv', 'ix', 'jg', 'jh', 'jhd',
	'jhds', 'jr', 'jur', 'k.a', 'k.k', 'k.u.k', 'kap', 'kgl', 'komp',
	'k\U000000F6nigl', 'ltd', 'm.a', 'm.e', 'm.sc', 'max', 'mdartl', 'med',
	'mhd', 'min', 'mind', 'mk', 'mndl', 'mod', 'mr', 'mrs', 'mwst', 'n',
	'n.a', 'n.chr', 'nb', 'nom', 'nr', 'o.a', 'o.g', 'o.\U000000E4', 'od',
	'p.a', 'p.p', 'p.s', 'perf', 'pers', 'pf', 'pfl', 'ph.d', 'phil', 'pl',
	'pr', 'prof', 'pr\U000000E4s', 'pr\U000000E4t', 'p\U000000E4d',
	'rer.medic', 'rer.nat', 'rer.pol', 'rer.soc', 'resp', 's', 's.a.e',
	's.a.s', 's.m.s', 's.o', 's.p.a', 's.r.l', 's.r.o', 's.s', 's.u',
	'sen', 'sg', 'sog', 'soz', 'sp', 'sr', 'st', 'std', 'stud', 'tab', 'u',
	'u.a', 'u.a.m', 'u.co', 'u.dergl', 'u.dgl', 'u.s', 'u.s.f', 'u.s.w',
	'u.u', 'u.v.m', 'u.\U000000E4', 'univ', 'usw', 'v', 'v.a', 'v.chr',
	'v.l', 'v.l.n.r', 'v.r', 'verf', 'vgl', 'vi', 'vii', 'viii', 'vs', 'x',
	'xi', 'xiii', 'xiv', 'xv', 'xvi', 'z', 'z.b', 'z.d', 'z.t', 'zit.n',
	'zus', 'zzgl', '\U000000FC'
]

sentTokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
sentTokenizer._params.abbrev_types.update(abbreviations)

inputDir = sys.argv[1]
outputDir = sys.argv[2]

inputDirEncoded = os.fsencode(inputDir)
outputDirEncoded = os.fsencode(outputDir)

unicodeParagraphSeparator = re.compile('\u2029')

paragraph = list()

for file in os.listdir(inputDirEncoded):
	# file: ohne inputDir davor; nur der Dateiname
	inputFile = os.path.join(inputDirEncoded, file)
	outputFile = os.path.join(outputDirEncoded, file)
	with open(outputFile, mode='w', encoding='utf-8', newline='\n') as output:
		with open(inputFile, mode='r', encoding='utf-8') as input:
			for line in input:
				start = 0
				while True:
					match = unicodeParagraphSeparator.search(line, start)
					if (match is None):
						break
					
					paragraph.append(line[start:match.start()])
					start = match.end()
					
					tokenizeParagraph(sentTokenizer, paragraph, output)
					paragraph.clear()
				
				if (start > 0):
					line = line[start:]
				line = line.strip()
				if line == '':
					tokenizeParagraph(sentTokenizer, paragraph, output)
					paragraph.clear()
				else:
					paragraph.append(line)
		tokenizeParagraph(sentTokenizer, paragraph, output)
		paragraph.clear()
		output.flush()
	print(os.fsdecode(file), end=' tokenized.\n')
