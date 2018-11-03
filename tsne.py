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

np.random.seed(1)

def annotate(image, words, n=float("inf")):
	for i, (label, x, y) in enumerate(zip(words, image[:, 0], image[:, 1])):
		if i == n: break
		plt.annotate(
			label,
			xy=(x, y), # xytext=(-20, 20),
			# textcoords='offset points', ha='right', va='bottom',
			# bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.5),
			# arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
			alpha=.4,
		)

def embed(words, model):
	return np.stack([model[word] for word in words], axis=0)

path = "models/voynich.bin"
model = fasttext.load_model(path)

words = list(model.words)
embedded = embed(words, model)

words_edy, words_ody, words_other = [], [], []
for word in words:
	if word.endswith("edy"):
		words_edy.append(word)
	elif word.endswith("ody"):
		words_ody.append(word)
	else:
		words_other.append(word)

embedded_edy = embed(words_edy, model)
embedded_ody = embed(words_ody, model)
embedded_other = embed(words_other, model)
embedded = np.concatenate([embedded_edy, embedded_ody, embedded_other], axis=0)

tsne = TSNE(n_components=2, metric="cosine")
image = tsne.fit_transform(embedded)
image_edy = image[:len(words_edy), :]
image_ody = image[len(words_edy):len(words_edy)+len(words_ody), :]
image_other = image[len(words_edy) + len(words_ody):, :]

plt.scatter(*zip(*image_edy), marker=".", c="r")
plt.scatter(*zip(*image_ody), marker=".", c="g")
plt.scatter(*zip(*image_other), marker=".", c="b")
# plt.scatter(*zip(*image), marker=".")

plt.title("Distribution of Words with -edy/-ody Suffix")
plt.legend(["-edy", "-ody", "other"])
# annotate(image, words_edy + words_ody + words_other)

plt.show()