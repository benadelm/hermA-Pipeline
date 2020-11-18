#!/bin/bash

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

WORKING_DIR="$(pwd)"
INPUT_DIR="$(readlink -m "$1")"
OUTPUT_DIR="$(readlink -m "$2")"

STICKER_DIR="$WORKING_DIR"/Sticker
STICKER_EXECUTABLE="$STICKER_DIR"/sticker
STICKER_CONFIG="$STICKER_DIR"/dep.conf

# sonst gibt Tensorflow diverse uninteressante Meldungen aus
export TF_CPP_MIN_LOG_LEVEL=2

cd "$INPUT_DIR" || exit

for FILENAME in *
do
	"$STICKER_EXECUTABLE" tag "$STICKER_CONFIG" --input "$INPUT_DIR"/"$FILENAME" --output "$OUTPUT_DIR"/"$FILENAME"
done