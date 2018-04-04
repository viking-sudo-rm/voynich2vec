import requests, re, os
from gensim.models.word2vec import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

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

Transcription:
Takahashi transcription. Our tokenization finds 37105 words.

Preprocessing:
Strip exclamation, percent
Ignore words with *

"""

# The letter after semicolon specifies which transcription to use. Options are H, C, F, N, U.
LINE_PATTERN = r"^\<.+H\>\s+(.+)$"
TRANSCRIPT = "text16e6.evt"

def getLines():
	with open(TRANSCRIPT, "r") as fh:
		lines = re.findall(LINE_PATTERN, fh.read(), re.MULTILINE)
		return [line.split(".") for line in lines]

if __name__ == "__main__":

	lines = getLines()

	# Should be 37919 according to
	# https://www.eleceng.adelaide.edu.au/personal/dabbott/wiki/images/8/82/Cracking_the_Voynich_Manuscript-_Using_basic_statistics_and_analyses_to_determine_linguistic_relationships.pdf
	print "Found {} words".format(sum(len(line) for line in lines))

	model = Word2Vec(lines,
		size=100,
		window=5,
		min_count=5,
		workers=4,
	)

	# Check the cosine similarity between two words
	print model.wv.similarity("qokal", "chcthy")

	X = model[model.wv.vocab]
	tsne = TSNE(n_components=2)
	Y = tsne.fit_transform(X)

	plt.scatter(Y[:, 0], Y[:, 1])
	plt.show()