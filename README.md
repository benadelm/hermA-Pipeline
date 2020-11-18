# hermA-Pipeline

This repository contains instructions for setting up the linguistic processing pipeline for German used in the research project [hermA](https://www.herma.uni-hamburg.de/en.html), as well as some models, data and helper scripts for running the tools.

The pipeline consists of the following stages:

1. **tokenization** (word/sentence splitting): This pipeline uses the [implementation of the PUNKT algorithm](https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.punkt) from Python’s [NLTK library](https://www.nltk.org/).
   * The algorithm itself is described in the paper <a href="https://www.mitpressjournals.org/doi/pdfplus/10.1162/coli.2006.32.4.485">Kiss, Tibor; Strunk, Jan (2006): <i>Unsupervised multilingual sentence boundary detection</i>. Computational linguistics, vol. 32, no. 4, MIT press, pp. 485–525</a>.
2. **part-of-speech and morphological tagging**: This pipeline uses a weighted ensemble of three different taggers, all of them trained on the [Tiger corpus](https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger/). Weight files for the weighted ensemble are provided with this repository. The taggers are:
   * [MarMoT](http://cistern.cis.lmu.de/marmot/), described in <a href="http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.593.7354&rep=rep1&type=pdf">Mueller, Thomas; Schmid, Helmut; Schütze, Hinrich (2013): <i>Efficient Higher-Order CRFs for Morphological Tagging</i>. Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pp. 322–332, Seattle, Washington, USA. Association for Computational Linguistics</a>.
   * [RFTagger](https://www.cis.uni-muenchen.de/~schmid/tools/RFTagger/), described in <a href="https://www.cis.uni-muenchen.de/~schmid/papers/Schmid-Laws.pdf">Schmid, Helmut; Laws, Florian (2008): <i>Estimation of Conditional Probabilities with Decision Trees and an Application to Fine-Grained POS Tagging</i>. In Scott, Donia; Uszkoreit, Hans (eds.): <i>Proceedings of the 22nd International Conference on Computational Linguistics</i>, Manchester, Great Britain</a>.
   * [HunPos](http://mokk.bme.hu/resources/hunpos/), described in <a href="https://eprints.sztaki.hu/7909/1/Kornai_196394_ny.pdf">Halácsy, Péter; Kornai, András; Oravecz, Csaba (2007): <i>HunPos – an open source trigram tagger</i>. Proceedings of the ACL 2007 Demo and Poster Sessions, pp. 209–212, Prague, Czech Republic. Association for Computational Linguistics</a>.
3. **lemmatization**: This pipeline uses the Python library [GermaLemma](https://github.com/WZBSocialScienceCenter/germalemma).
4. **dependency parsing**: This pipeline uses [sticker](https://github.com/stickeritis/sticker) with a model trained on the [Hamburg Dependency Treebank (HDT)](https://nats-www.informatik.uni-hamburg.de/HDT/WebHome).

These third-party tools are not included in this repository, you have to obtain them separately and place them in the directory structure provided by this repository (see installation instructions below).

# System Requirements

The pipeline has been used with Linux. It employs Bash and Python scripts, so you will need a Bash interpreter and a Python interpreter. Furthermore you will need a Java runtime for the POS converter and ensemble (developed and tested with Java 8, newer versions may also work). In addition, the third-party tools used in the pipeline stages have their own system requirements.

# Installation

## Tokenizer

Make sure you have Python 3 and the NLTK library installed. NLTK can be installed with PIP: `pip3 install nltk` (or `pip3 install --user nltk` if you are not an administrator/superuser). See [Installing NLTK](https://www.nltk.org/install.html) if you need additional instructions.

Install PUNKT if it is not installed yet. This can be done from within a Python interpreter:

	import nltk
	nltk.download('punkt')

The NLTK implementation of PUNKT will be used by the Python script `Tools/Tokenizer/tokenizer.py` from this repository.

## Taggers

### MarMoT

MarMoT can be obtained [here](http://cistern.cis.lmu.de/marmot/bin/CURRENT/). Copy the `.jar` file whose name starts with `marmot` to the `Tools/Tagger/MarMoT` directory and rename it to `marmot.jar`.

Download [the MarMoT model for German](http://cistern.cis.lmu.de/marmot/models/CURRENT/spmrl/de.marmot) and place it in the `Tools/Tagger/MarMoT` directory, too.

### RFTagger

RFTagger can be downloaded [here](https://www.cis.uni-muenchen.de/~schmid/tools/RFTagger/data/RFTagger.tar.gz). Unpack the file and copy the `RFTagger/bin/rft-annotate` binary to the `Tools/Tagger/RFTagger` directory. A model is provided with this repository.

### HunPos

HunPos can be downloaded [here](https://code.google.com/archive/p/hunpos/downloads). Unpack the file and copy the `hunpos-tag` binary to the `Tools/Tagger/HunPos` directory. A model is provided with this repository.

### Tag converter

Compile [this converter](https://github.com/benadelm/GermanPOSTagConverter) to a `.jar` file or download an already compiled one from a [release](https://github.com/benadelm/GermanPOSTagConverter/releases). The file name of the `.jar` should be `Tag-Konverter.jar`. Place it in the `Tools/Tagger` directory.

## Lemmatizer

[GermaLemma](https://github.com/WZBSocialScienceCenter/germalemma) can be installed with PIP: `pip3 install germalemma` (or `pip3 install --user germalemma` if you are not an administrator/superuser). GermaLemma will be used by the Python script `Tools/Lemmatizer/germalemma_lemmatize_conllx_fallback_dir.py` from this repository.

## Parser

Obtain sticker from the [repository](https://github.com/stickeritis/sticker). There are some [releases](https://github.com/stickeritis/sticker/releases); the models provided here have been created with [the version 0.10.0 release](https://github.com/stickeritis/sticker/releases/tag/0.10.0), so try that release if a newer version does not work.

After cloning/downloading the repository and compiling sticker, or after unpacking the release download, respectively, place the `sticker` binary (`sticker-0.10.0-x86_64-unknown-linux-gnu/sticker` for the Linux version of the version 0.10.0 release) in the `Tools/Parser/Sticker` directory. Do the same for the files starting with `libtensorflow` (`libtensorflow.so` and so on). Note that some of these files are softlinks.

Download [these](https://github.com/stickeritis/sticker-models/releases/tag/de-structgram-20190426-opq) German word embeddings and place them in the `Tools/Parser/Sticker/embeddings` directory. The file name should be `de-structgram-20190426-opq.fifu` (or you will have to adjust line 7 of `Tools/Parser/Sticker/dep.conf`). The `.asc` file is not needed.

Side note: The part-of-speech tag embedding `Tools/Parser/Sticker/embeddings/postags.fifu` is effectively [this](https://blob.danieldk.eu/sticker-models/de-structgram-tags-20190426.fifu) one, but with `PROP` renamed to `PAV` to be consistent with the output of the tagging stage.

# Usage

Before running the pipeline, the `Pipeline` directory should be empty except for sub-directories (that is, there should be no files, neither in the directory itself nor in some sub-directory). The shell script `clear.sh` can be used to delete all files in the relevant directories, **including input and output directory** (so please make sure first your input and output files have been saved elsewhere).

To run the pipeline, put raw texts (UTF-8 plain text files) to be processed in the `Pipeline/00_input` directory. Then run `bash Pipeline.sh`.

The pipeline stages are processed one after the other, so first all files in the input directory are tokenized, then (after all of them have been tokenized) all tokenized texts are tagged, and so on. The final output (after the dependency parsing step) will be written to the `Pipeline/04_parse` directory. File names, including extensions, are not changed, so the files in the output directory will have exactly the same names as the corresponding input files. Pipeline stage outputs are aggregated, so the parser output also contains the part-of-speech tags, morphological annotations and lemmata.