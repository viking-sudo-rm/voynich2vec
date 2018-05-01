#!/usr/bin/env python
#
# compute high-tfidf words in the voynich

import vms_tokenize
from collections import Counter, defaultdict, OrderedDict
from math import log

def term_freq(term, page):
	return term_counts[page][term]

def inv_doc_freq(term):
	return log(float(len(pages)) / len(doc_counts[term]))

def tfidf(term, page):
	return term_freq(term, page) * inv_doc_freq(term)

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

astro = ['f57v',
		 'f67r1', 'f67r2', 'f67v1', 'f67v2',
		 'f68r1', 'f68r2', 'f68r3', 'f68v1', 'f68v2', 'f68v3',
		 'f69r', 'f69v',
		 'f70r1', 'f70r2', 'f70v1', 'f70v2',
		 'f71r', 'f71v',
		 'f72r1', 'f72r2', 'f72r3', 'f72v1', 'f72v2', 'f72v3',
		 'f73r', 'f73v',
		 'f85r1', 'f85r2',
		 'f86v3', 'f86v4',
		 ]

# count terms on page
for p in astro:
	words = []
	for w in list(term_counts[p]):
		words.append((w, tfidf(w, p)))

	words.sort(key=lambda x: x[1], reverse=True)
	print p
	for w, v in words[:5]:
		print "\t", w, "\t", v


# TSNE

