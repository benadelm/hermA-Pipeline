#!/bin/bash

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

WORKING_DIR="$(pwd)"
INPUT_DIR="$(readlink -m "$1")"
OUTPUT_DIR="$(readlink -m "$2")"

MARMOT_DIR="$WORKING_DIR"/MarMoT
MARMOT_JAR="$MARMOT_DIR"/marmot.jar
MARMOT_MODEL="$MARMOT_DIR"/de.marmot
MARMOT_CONFUSION="$MARMOT_DIR"/confusion
MARMOT_OUTPUT_DIR="$OUTPUT_DIR"/MarMoT/CoNLL2009

RFTAGGER_DIR="$WORKING_DIR"/RFTagger
RFTAGGER_EXECUTABLE="$RFTAGGER_DIR"/rft-annotate
RFTAGGER_MODEL="$RFTAGGER_DIR"/model.par
RFTAGGER_CONFUSION="$RFTAGGER_DIR"/confusion
RFTAGGER_OUTPUT_DIR="$OUTPUT_DIR"/RFTagger
RFTAGGER_OUTPUT_DIR_TIGER="$RFTAGGER_OUTPUT_DIR"/Tiger
RFTAGGER_OUTPUT_DIR_CONLL="$RFTAGGER_OUTPUT_DIR"/CoNLL2009

HUNPOS_DIR="$WORKING_DIR"/HunPos
HUNPOS_EXECUTABLE="$HUNPOS_DIR"/hunpos-tag
HUNPOS_MODEL="$HUNPOS_DIR"/model
HUNPOS_CONFUSION="$HUNPOS_DIR"/confusion
HUNPOS_OUTPUT_DIR="$OUTPUT_DIR"/HunPos
HUNPOS_OUTPUT_DIR_TIGER="$HUNPOS_OUTPUT_DIR"/Tiger
HUNPOS_OUTPUT_DIR_CONLL="$HUNPOS_OUTPUT_DIR"/CoNLL2009

ENSEMBLE_OUTPUT_DIR="$OUTPUT_DIR"/Ensemble

TAGCORR_PY="$WORKING_DIR"/correctMarMoTTags.py
TAGCONV_JAR="$WORKING_DIR"/Tag-Konverter.jar
ENSEMBLE_JAR="$WORKING_DIR"/weightedPosMorphEnsemble.jar

cd "$INPUT_DIR" || exit

for FILENAME in *
do
	INPUT_FILE="$INPUT_DIR"/"$FILENAME"
	
	# MarMoT
	MARMOT_IN_TEMP="$(mktemp -p "$MARMOT_OUTPUT_DIR" MarMoTinXXXXXXXXXXXXXXXX.txt)"
	ln -s -f "$INPUT_FILE" "$MARMOT_IN_TEMP"
	MARMOT_OUT_TEMP="$(mktemp -p "$MARMOT_OUTPUT_DIR" MarMoToutXXXXXXXXXXXXXXXX.txt)"
	java -Dfile.encoding=UTF-8 -cp "$MARMOT_JAR" marmot.morph.cmd.Annotator --model-file "$MARMOT_MODEL" --test-file "form-index=0,$MARMOT_IN_TEMP" --pred-file "$MARMOT_OUT_TEMP"
	rm "$MARMOT_IN_TEMP"
	python3 "$TAGCORR_PY" "$MARMOT_OUT_TEMP" "$MARMOT_OUTPUT_DIR"/"$FILENAME"
	rm "$MARMOT_OUT_TEMP"
	
	# RFTagger
	RFTAGGER_OUTPUT_FILE="$RFTAGGER_OUTPUT_DIR_TIGER"/"$FILENAME"
	"$RFTAGGER_EXECUTABLE" "$RFTAGGER_MODEL" "$INPUT_FILE" "$RFTAGGER_OUTPUT_FILE"
	java -jar "$TAGCONV_JAR" -input-charset utf-8 -output-charset utf-8 -input-format rftagger -output-format conllx "$RFTAGGER_OUTPUT_FILE" "$RFTAGGER_OUTPUT_DIR_CONLL"/"$FILENAME"
	
	# HunPos
	HUNPOS_OUTPUT_FILE="$HUNPOS_OUTPUT_DIR_TIGER"/"$FILENAME"
	"$HUNPOS_EXECUTABLE" "$HUNPOS_MODEL" < "$INPUT_FILE" > "$HUNPOS_OUTPUT_FILE"
	java -jar "$TAGCONV_JAR" -input-charset utf-8 -output-charset utf-8 -input-format rftagger -output-format conllx "$HUNPOS_OUTPUT_FILE" "$HUNPOS_OUTPUT_DIR_CONLL"/"$FILENAME"
done

# Ensemble
java -jar "$ENSEMBLE_JAR" "$ENSEMBLE_OUTPUT_DIR" "$MARMOT_OUTPUT_DIR" "$MARMOT_CONFUSION" "$RFTAGGER_OUTPUT_DIR_CONLL" "$RFTAGGER_CONFUSION" "$HUNPOS_OUTPUT_DIR_CONLL" "$HUNPOS_CONFUSION"