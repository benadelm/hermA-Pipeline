#!/bin/bash

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

# Löscht alle Dateien aus den Pipeline-Verzeichnissen
# INKLUSIVE INPUT- UND OUTPUT-VERZEICHNIS (!)

cd Pipeline/00_input
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../..

cd Pipeline/01_tokens
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../..

cd Pipeline/02_tags
cd MarMoT/CoNLL2009
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../../RFTagger/CoNLL2009
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../Tiger
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../../HunPos/CoNLL2009
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../Tiger
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../../Ensemble
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../../..

cd Pipeline/03_lemmata
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../..

cd Pipeline/04_parse
for FILENAME in *
do
	[ -f "$FILENAME" ] || continue
	rm "$FILENAME"
done
cd ../..