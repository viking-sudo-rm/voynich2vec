import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re, io

FIN = "corpora/perseus/Classics/Galen/opensource/gal.nat.fac_gk.xml"
FOUT = "texts/galen.txt"

with open(FIN, "r") as fh:
	doc = fh.read()

# Requires pip install lxml
soup = BeautifulSoup(doc, "lxml")
text = soup.find("body").get_text().strip()

print text

with io.open(FOUT, "w", encoding="utf-8") as fh:
	fh.write(unicode(text))