import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import fasttext
import argparse

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

TEXT = "secretaSecretorum"
FORMAT = "bin" # "vec"
NATIVE = "models/{}.{}".format(TEXT, FORMAT)
MAPPED = "alignments/{}/vectors-vy.txt".format(TEXT)

# SRC = "models/voynich.bin"
# TRG = "alignments/secretaSecretorum/vectors-la.txt"

model = fasttext.load_model(NATIVE)
print "Got model"
words_la = list(model.words)
embed_la = np.stack([model[word] for word in words_la], axis=0)
print "Got native embeddings"

words_vy, embed_vy = load_aligned(MAPPED)
print "Got mapped embeddings"

sims = np.dot(embed_vy, embed_la.T)
indices = np.flip(np.argsort(sims, axis=1), axis=1)[:,:5]

for i, w_vy in enumerate(words_vy):
	print w_vy, [words_la[j] for j in indices[i,:]]
print indices.shape

embed = np.concatenate([embed_vy, embed_la], axis=0)
tsne = TSNE(n_components=2)
image = tsne.fit_transform(embed)
image_vy = image[:len(embed_vy),:]
image_la = image[len(embed_vy):,:]

zip(*image_vy)

plt.scatter(image_vy[:, 0], image_vy[:, 1], c="r")
plt.scatter(image_la[:, 0], image_la[:, 1], c="g")
plt.savefig("images/{}.png".format(TEXT))
