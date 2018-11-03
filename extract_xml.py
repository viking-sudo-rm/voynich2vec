"""

Extract plain text of texts encoded in XML format.

For Perseus or Bible corpus, use `--format body` (default).

"""

from bs4 import BeautifulSoup
import argparse, io

parser = argparse.ArgumentParser(description='Extract plain text from XML-formatted files.')
parser.add_argument("--read_xml", type=str, required=True)
parser.add_argument("--save_text", type=str, required=True)
parser.add_argument("--format", type=str, default="body")

def body(soup):
	return soup.find("body").get_text().strip()

if __name__ == "__main__":

	args = parser.parse_args()
	print "Input XML:", args.read_xml
	print "Output text:", args.save_text
	print "Format:", args.format

	with open(args.read_xml) as fh:
		soup = BeautifulSoup(fh.read(), "lxml")

	# Extract using the right format
	text = vars()[args.format](soup)
	print text

	with io.open(args.save_text, "w", encoding="utf-8") as fh:
		fh.write(unicode(text))


	