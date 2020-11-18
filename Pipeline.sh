#!/bin/bash

# This Source Code Form is subject to the terms of the hermA Licence.
# If a copy of the licence was not distributed with this file, You have
# received this Source Code Form in a manner that does not comply with
# the terms of the licence.

INPUT_DIR="Pipeline/00_input"
TOKENS_DIR="Pipeline/01_tokens"
TAGS_IN_DIR="Pipeline/02_tags"
TAGS_OUT_DIR="$TAGS_IN_DIR/Ensemble"
LEMMATA_DIR="Pipeline/03_lemmata"
PARSE_DIR="Pipeline/04_parse"

# tokenize
cd Tools/Tokenizer
python3 tokenizer.py ../../"$INPUT_DIR" ../../"$TOKENS_DIR" || exit
cd ../..

# tag
cd Tools/Tagger
bash tag.sh ../../"$TOKENS_DIR" ../../"$TAGS_IN_DIR" || exit
cd ../..

# lemmatize
cd Tools/Lemmatizer
python3 germalemma_lemmatize_conllx_fallback_dir.py ../../"$TAGS_OUT_DIR" ../../"$LEMMATA_DIR" Vollformen_geschlossene_Wortklassen_final.txt || exit
cd ../..

# parse
cd Tools/Parser
bash parse.sh ../../"$LEMMATA_DIR" ../../"$PARSE_DIR" || exit
cd ../..
