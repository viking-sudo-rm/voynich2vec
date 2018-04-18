#!/usr/bin/env python
import requests, re, os, io
from gensim.models.word2vec import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from nltk import sent_tokenize, word_tokenize
import fasttext

import vms_tokenize

"""

Notes:

Word2Vec on Voynich:
http://blog.christianperone.com/2016/01/voynich-manuscript-word-vectors-and-t-sne-visualization-of-some-patterns/

Gensim Word2Vec:
https://radimrehurek.com/gensim/models/word2vec.html
https://machinelearningmastery.com/develop-word-embeddings-python-gensim/

Punctuation in the Voynich:
https://stephenbax.net/?p=940

Multilingual word embeddings:
https://arxiv.org/pdf/1710.04087.pdf
https://github.com/Kyubyong/wordvectors

https://github.com/facebookresearch/fastText
https://github.com/facebookresearch/MUSE
Note that src_lang and trg_lang don't get used in unsupervised!

Transcription:
Takahashi transcription. Our tokenization finds 37105 words.

Preprocessing:
Strip exclamation, percent
Ignore words with *

"""

TRANSCRIPT = "text16e6.evt"
# LINE_PATTERN = r"^\<.+H\>\s+(.+)$"
# TOKENIZE_PATTERN = r"[\.,-=]"
# IGNORE_PATTERN = r"[*%]"
# STRIP_PATTERN = r"[!%]|(\{.*\})"

def cleanup(line):
	line = re.sub(STRIP_PATTERN, "", line)
	tokens = re.split(TOKENIZE_PATTERN, line)
	return filter(lambda w: w, tokens)

def getLines():
	with open(TRANSCRIPT, "r") as fh:
		lines = re.findall(LINE_PATTERN, fh.read(), re.MULTILINE)
		return map(cleanup, lines)

def getVoynichModel():

	# lines = getLines()
	# print "First line: {}".format(lines[0])

	# # Should be 37919 according to
	# # https://www.eleceng.adelaide.edu.au/personal/dabbott/wiki/images/8/82/Cracking_the_Voynich_Manuscript-_Using_basic_statistics_and_analyses_to_determine_linguistic_relationships.pdf
	# print "Found {} words".format(sum(len(line) for line in lines))

	with open("temp.txt", "w") as fh:
		for line in vms_tokenize.get_words(TRANSCRIPT):
			fh.write(" ".join(line) + "\n")

	print "Training models/voynich"
	model = fasttext.skipgram('temp.txt', 'models/voynich')
	print model.words
	return model

def getOtherModel(name):

	with io.open("texts/{}.txt".format(name), encoding="utf-8") as fh:
		text = fh.read()

	with io.open("temp.txt".format(name), "w", encoding="utf-8") as fh:
		for sent in sent_tokenize(text):
			fh.write(" ".join(word_tokenize(sent)) + "\n")

	print "Training models/" + name
	model = fasttext.skipgram("temp.txt", "models/" + name)
	print model.words
	return model

if __name__ == "__main__":

	# model = Word2Vec(lines,
	# 	size=100,
	# 	window=5,
	# 	min_count=5,
	# 	workers=4,
	# )

	# print "Found {} vocab items".format(len(model.wv.vocab))

	# # Check the cosine similarity between two words
	# print model.wv.similarity("qokal", "chcthy")

	# model = getVoynichModel()
	model = getOtherModel("secretaSecretorum")

	X = np.array([model[w] for w in model.words])
	print "Embedding shape", X.shape

	# X = model[model.wv.vocab]
	tsne = TSNE(n_components=2)
	Y = tsne.fit_transform(X)

	# plt.scatter(Y[:, 0], Y[:, 1])
	# plt.show()
