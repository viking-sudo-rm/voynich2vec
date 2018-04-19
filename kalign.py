#!/usr/bin/python
import io
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import fasttext
import argparse

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

load_aligned = lambda file_path: list(gen_aligned(file_path))		

parser = argparse.ArgumentParser(description='Build vectors for documents.')
parser.add_argument("--text", type=str, default=None)
parser.add_argument("--format", type=str, default="bin")
args = parser.parse_args()

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

sims = np.dot(embed_vy, embed_la.T)
indices = np.flip(np.argsort(sims, axis=1), axis=1)[:,:5]

filename = "alignments/{}.txt".format(args.text)
with io.open(filename, "w", encoding="utf-8") as fh:
	for i, w_vy in enumerate(words_vy):
		fh.write(unicode(w_vy))
		fh.write(u"\t")
		fh.write(u"\t".join(words_la[j] for j in indices[i,:]))
		fh.write(u"\n")
print "Saved alignment to", filename

embed = np.concatenate([embed_vy, embed_la], axis=0)

print "Doing TSNE"
tsne = TSNE(n_components=2)
image = tsne.fit_transform(embed)
image_vy = image[:len(embed_vy),:]
image_la = image[len(embed_vy):,:]

plt.scatter(*zip(*image_vy), c="r")
plt.scatter(*zip(*image_la), c="g")
plt.title(args.text)

filename = "images/{}.png".format(args.text)
plt.savefig(filename)
print "Saved TSNE image to", filename
plt.show()