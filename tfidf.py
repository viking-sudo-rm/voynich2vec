#!/usr/bin/env python
#
# compute high-tfidf words in the voynich

import vms_tokenize
from collections import Counter, defaultdict, OrderedDict
from math import log

import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import fasttext
import argparse
import sys

from section_labels import *

def term_freq(term, page):
	# raw count
	# return term_counts[page][term]

	# normalize by page length
	return float(term_counts[page][term]) / sum(term_counts[page].values())

	# normalize by most common word
	# return float(term_counts[page][term]) / max(term_counts[page].values())

def inv_doc_freq(term):
	return log(float(len(pages)) / len(doc_counts[term]))

def tfidf(term, page):
	return term_freq(term, page) * inv_doc_freq(term)


def annotate(image, words, n=float("inf")):
	annotation_list = []
	for i, (label, x, y) in enumerate(zip(words, image[:, 0], image[:, 1])):
		if i == n: break
		plt.annotate(
			label,
			xy=(x, y), # xytext=(-20, 20),
			alpha = 0.4,
			# textcoords='offset points', ha='right', va='bottom',
			# bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.5),
			# arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
		)

def embed(words, model):
	return np.stack([model[word] for word in words], axis=0)


path = "models/voynich.bin"
model = fasttext.load_model(path)
vecwords = set(model.words)

term_counts = defaultdict(Counter)
doc_counts = defaultdict(set)

# really this should be a set, but we want ordering
pages = OrderedDict()

# load words
for line in vms_tokenize.get_words("text16e6.evt", page_numbers=True):
	pg = line.pop(0)
	pages[pg] = True

	term_counts[pg].update(line)
	for word in line:
		doc_counts[word].add(pg)


overall = []

tsne_words = OrderedDict([('text',[]), ('herbal',[]), ('astro',[]), ('bath',[]), ('multiherbal',[])])
embedded = OrderedDict()

# count terms on page
for p in pages:
	if section_labels[p] != 'herbal':
		continue

	words = []
	for w in list(term_counts[p]):
		# if term_counts[p][w] <= 2:
		# 	continue
		ti = tfidf(w, p)
		words.append((w, ti))
		overall.append((p, w, ti))

	words.sort(key=lambda x: x[1], reverse=True)
	print p
	for w, v in words[:5]:
		print "\t", w, "\t", v, "\t", term_counts[p][w]
		if w in vecwords:
			if w not in tsne_words[section_labels[p]]:
				tsne_words[section_labels[p]].append(w)

# TODO: only show highest ranked if in many categories.

print "top overall"
overall.sort(key = lambda x: x[2], reverse=True)
for p, w, v in overall[:40]:
	print p, w, v, term_counts[p][w]
	# if w in vecwords:
	# 	tsne_words[section_labels[p]].append(w)

#print(tsne_words)

sys.exit()

for k, v in tsne_words.items():
	if not v: continue
	embedded[k] = embed(v, model)

embedded = np.concatenate([v for v in embedded.values()], axis=0)

tsne = TSNE(n_components=2, metric="cosine")
image = tsne.fit_transform(embedded)

annotate(image, tsne_words['text'] + tsne_words['herbal'] + tsne_words['astro'] + tsne_words['bath'] + tsne_words['multiherbal']) 

plt.scatter(*zip(*image), c = ["grey"] * len(tsne_words['text']) +
							  ["green"] * len(tsne_words['herbal']) +
							  ["red"] * len(tsne_words['astro']) +
							  ["yellow"] * len(tsne_words['bath']) + 
							  ["blue"] * len(tsne_words['multiherbal']))

plt.show()

