#!/usr/bin/python
import io
import numpy as np
import numpy.linalg as npla
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import fasttext
import argparse
import sys
import math

path = "models/voynich.bin"
model = fasttext.load_model(path)

words = list(model.words)
vectors = np.array([model[w] for w in words])

mag = npla.norm(vectors, axis=1)[:,None] * npla.norm(vectors, axis=1)

sims = np.divide(np.dot(vectors, vectors.T), mag)
sims = np.tril(sims, -1) # don't align to self and remove dups
indices = np.flip(np.argsort(sims, axis=1), axis=1)[:,:5]

word_dist = []
for i, w in enumerate(words):
	L = [(w.encode('utf-8'), words[j].encode('utf-8'), math.acos(sims[i, j])) for j in indices[i, :]]
	word_dist.extend(L)
	# print w
	# for _, match, dist in L:
	# 	print "\t", match, "\t", dist

word_dist.sort(key = lambda x: x[2])

# for w in word_dist:
# 	print w[0], "\t", w[1], "\t", w[2]

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

tsne = TSNE(n_components=2, metric='cosine')
image = tsne.fit_transform(vectors)

plt.scatter(*zip(*image), c="r", marker='.')

coords = dict(zip(words, image))

for w in word_dist:
	a = coords[w[0]]
	b = coords[w[1]]
	plt.plot((a[0], b[0]), (a[1], b[1]), alpha=0.15)

plt.title('voynich self-alignment')

annotate(image, words)

plt.show()