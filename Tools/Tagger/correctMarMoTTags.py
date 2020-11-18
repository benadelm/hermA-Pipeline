#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

# Converts $LRB to $( and PROAV to PAV in MarMoT outputs (CoNLL-2009),
# deduplicates the POS tag (e.g. 'NN|NN' -> 'NN'),
# removes redundant mood=imp features
# and produces a CoNLL-X file

import os, sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]

inputFileEncoded = os.fsencode(inputFile)
outputFileEncoded = os.fsencode(outputFile)

def deduplicate(pos):
	pipePos = pos.find('|')
	if pipePos < 0:
		return pos
	return pos[:pipePos]

impStr = 'mood=imp'
impStrLen = len(impStr)

def removeImp(morph):
	impPos = morph.find(impStr)
	if impPos < 0:
		return morph
	if impPos > 0:
		impPos = impPos - 1
		if morph[impPos] != '|':
			return morph
	return morph[:impPos] + morph[(impPos + impStrLen):]

with open(outputFileEncoded, mode='w', encoding='utf-8', newline='\n') as output:
	with open(inputFileEncoded, mode='r', encoding='utf-8') as input:
		for line in input:
			parts = line.rstrip('\n').split('\t')
			if len(parts) > 7:
				output.write(parts[0])
				output.write('\t')
				output.write(parts[1])
				output.write('\t')
				output.write(parts[3])
				output.write('\t_\t')
				output.write(deduplicate(parts[5]).replace('$LRB', '$(').replace('PROAV', 'PAV'))
				output.write('\t')
				output.write(removeImp(parts[7]))
				output.write('\t_\t_\t_\t_\n')
			else:
				output.write(line)
	output.flush()