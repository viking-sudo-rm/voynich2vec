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

# matplotlib.use('Agg')

def gen_aligned(file_path, n=float("inf")):
	words = []
	vecs = []
	with open(file_path) as fh:
		fh.readline() # ignore first line
		for i, line in enumerate(fh.readlines()):
			if i == n: break
			vec = line.split()
			words.append(vec[0])
			vecs.append(np.array(map(float, vec[1:])))
	return words, np.stack(vecs, axis=0)

def annotate(image, words, n=float("inf")):
	for i, (label, x, y) in enumerate(zip(words, image[:, 0], image[:, 1])):
		if i == n: break
		plt.annotate(
			label,
			xy=(x, y), # xytext=(-20, 20),
			# textcoords='offset points', ha='right', va='bottom',
			# bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.5),
			# arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
		)

load_aligned = lambda file_path: list(gen_aligned(file_path))		

parser = argparse.ArgumentParser(description='Build vectors for documents.')
parser.add_argument("--text", type=str, default="secretaSecretorum")
parser.add_argument("--format", type=str, default="bin")
parser.add_argument("--metric", type=str, default="cosine")
parser.add_argument("--labels", action="store_true")
args = parser.parse_args()
print(args)

native = "models/{}.{}".format(args.text, args.format)
mapped = "mappings/{}/vectors-vy.txt".format(args.text)

print "Native:", native
print "Mapped:", mapped

model = fasttext.load_model(native)
words_la = list(model.words)
embed_la = np.stack([model[word] for word in words_la], axis=0)
print "Got native embeddings"

words_vy, embed_vy = load_aligned(mapped)
print "Got mapped embeddings"

mag = npla.norm(embed_vy, axis=1)[:,None] * npla.norm(embed_la, axis=1).transpose()

# sims = np.dot(embed_vy, embed_la.T)
sims = np.divide(np.dot(embed_vy, embed_la.T), mag)
indices = np.flip(np.argsort(sims, axis=1), axis=1)[:,:5]

word_dist = []

filename = "alignments/{}.txt".format(args.text)
with io.open(filename, "w", encoding="utf-8") as fh:
	for i, w_vy in enumerate(words_vy):
		word_dist.extend([(w_vy, str(words_la[j]), math.acos(sims[i, j])) for j in indices[i, :]])
		fh.write(unicode(w_vy))
		fh.write(u"\t")
		fh.write(u"\t".join(words_la[j] for j in indices[i,:]))
		fh.write(u"\n")
		fh.write(u"\t" + u"\t".join(str(math.acos(sims[i, j])) for j in indices[i, :]))
		fh.write(u"\n")
print "Saved alignment to", filename

word_dist.sort(key = lambda x: x[2])

# for w in word_dist:
# 	print w[0], "\t", w[1], "\t", w[2]

embed = np.concatenate([embed_vy, embed_la], axis=0)

print "Doing TSNE.."
tsne = TSNE(n_components=2, metric=args.metric)
embed = np.concatenate([embed_vy, embed_la], axis=0)
image = tsne.fit_transform(embed)
image_vy = image[:len(embed_vy),:]
image_la = image[len(embed_vy):,:]

plt.scatter(*zip(*image_vy), c="r", marker='.')
plt.scatter(*zip(*image_la), c="g", marker='.')

vycoords = dict(zip(words_vy, image_vy))
lacoords = dict(zip(words_la, image_la))

for w in word_dist:
	# w[0] voynich
	# w[1] latin
	v = vycoords[w[0]]
	l = lacoords[w[1]]
	plt.plot((v[0], l[0]), (v[1], l[1]), alpha=0.1)

plt.title(args.text)

# filename = "images/{}.png".format(args.text)
# plt.savefig(filename)

if args.labels:
	annotate(image_vy, words_vy)
	annotate(image_la, words_la)

# print "Saved TSNE image to", filename
plt.show()