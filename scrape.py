import requests

"""

Notes:

Word2Vec on Voynich:
http://blog.christianperone.com/2016/01/voynich-manuscript-word-vectors-and-t-sne-visualization-of-some-patterns/

Gensim Word2Vec:
https://radimrehurek.com/gensim/models/word2vec.html
https://machinelearningmastery.com/develop-word-embeddings-python-gensim/

The transcription should be obtained by scraping www.voynich.nu.

The page for quire 1 can be found at

	http://www.voynich.nu/q01/q01_tr.txt.

"""

FORMAT = "http://www.voynich.nu/q{:02d}/q{:02d}_tr.txt"
TRANSCRIPT_FORMAT = "transcript/q{:02d}_tr.txt"

def scrape():
	for quire in xrange(1, 1000):
		url = FORMAT.format(quire, quire)
		res = requests.get(url)
		print "Querying {}..".format(url)
		if res.status_code == 404: break # Side of folio doesn't exist
		with open(TRANSCRIPT_FORMAT.format(quire), "w") as fh:
			fh.write(res.text.encode("utf-8"))
	print "Found {} quires".format(quire - 1)

if __name__ == "__main__":
	scrape()