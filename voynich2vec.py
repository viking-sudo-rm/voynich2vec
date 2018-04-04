import requests, re, os
from gensim.models.word2vec import Word2Vec

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

# FORMAT = "http://www.voynich.nu/q{:02d}/q{:02d}_tr.txt"
# TRANSCRIPT_FORMAT = "transcript/q{:02d}_tr.txt"

# def scrape():
# 	for quire in xrange(1, 1000):
# 		url = FORMAT.format(quire, quire)
# 		res = requests.get(url)
# 		print "Querying {}..".format(url)
# 		if res.status_code == 404: break # Quire doesn't exist
# 		with open(TRANSCRIPT_FORMAT.format(quire), "w") as fh:
# 			fh.write(res.text.encode("utf-8"))
# 	print "Found {} quires".format(quire - 1)

# Note: The letter after semicolon specifies which transcription to use. Options are H, C, F, N, U.
LINE_PATTERN = r"^\<.+H\>\s+(.+)$"
TRANSCRIPT = "text16e6.evt"

def getLines():
	with open(TRANSCRIPT, "r") as fh:
		lines = re.findall(LINE_PATTERN, fh.read(), re.MULTILINE)
		return [line.split(".") for line in lines]

if __name__ == "__main__":

	lines = getLines()

	# According to https://www.eleceng.adelaide.edu.au/personal/dabbott/wiki/images/8/82/Cracking_the_Voynich_Manuscript-_Using_basic_statistics_and_analyses_to_determine_linguistic_relationships.pdf, should find 37919
	print "Found {} words".format(sum(len(line) for line in lines))

	model = Word2Vec(lines,
		size=100,
		window=5,
		min_count=5,
		workers=4,
	)

	# Example model similarity
	print model.wv.similarity("qokal", "chcthy")