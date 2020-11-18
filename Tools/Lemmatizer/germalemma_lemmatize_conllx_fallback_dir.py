#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

import os, sys
from germalemma import GermaLemma

inputDir = sys.argv[1]
outputDir = sys.argv[2]
fallbackTable = sys.argv[3]

inputDirEncoded = os.fsencode(inputDir)
outputDirEncoded = os.fsencode(outputDir)

fallback = {}
with open(fallbackTable, 'r') as ffb:
	for line in ffb:
		parts = line.strip().split("\t")
		form = parts[0].lower()
		pos = parts[1]
		lemma = parts[2]
		if form in fallback:
			postable = fallback[form]
		else:
			postable = {}
			fallback[form] = postable
		postable[pos] = lemma

fallback2 = {}
for form, subtable in fallback.items():
	if len(subtable) == 1:
		for lemma in subtable.values():
			fallback2[form] = lemma

def useFallback(form, pos):
	formLower = form.lower()
	if formLower in fallback:
		subtable = fallback[formLower]
		if pos in subtable:
			return subtable[pos]
		if formLower in fallback2:
			return fallback2[formLower]
	return form

lemmatizer = GermaLemma()

for file in os.listdir(inputDirEncoded):
	# file: ohne inputDir davor; nur der Dateiname
	inputFile = os.path.join(inputDirEncoded, file)
	outputFile = os.path.join(outputDirEncoded, file)
	with open(outputFile, mode='w', encoding='utf-8', newline='\n') as fout:
		with open(inputFile, mode='r', encoding='utf-8') as fin:
			for line in fin:
				line_stripped = line.strip()
				if (line_stripped != ''):
					parts = line_stripped.split('\t')
					form = parts[1]
					pos = parts[4]
					fout.write(parts[0])
					fout.write('\t')
					fout.write(form)
					fout.write('\t')
					try:
						lemma = lemmatizer.find_lemma(form, pos)
					except ValueError:
						lemma = useFallback(form, pos)
					fout.write(lemma)
					fout.write('\t_\t')
					fout.write(pos)
					fout.write('\t')
					fout.write(parts[5])
					fout.write('\t')
					fout.write(parts[6])
					fout.write('\t')
					fout.write(parts[7])
					fout.write('\t_\t_')
				fout.write('\n')
		fout.flush()
