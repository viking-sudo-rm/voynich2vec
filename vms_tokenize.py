# Takahashi Tokenizer
# by Eli Baum

# TODO:
# 89r2 paragraph issue
# column breaks \
#	34r probably fine
#	39r definitely fine
#	89r2 looks like different paragraph?

from collections import Counter
import re, io

def get_words(file, page_numbers=False):
	with io.open(file, 'r', encoding="latin_1") as file:
		for line in file.read().splitlines():
			# pull out page numbers
			# if page_numbers:
			# 	m = re.match(r'^<(f\d+[rv].?)>', line)

			# 	if m:
			# 		pg = str(m.group(1))
			# 		yield ['#', pg]

			# pull out takahashi lines
			m = re.match(r'^<(f.*?)\..*;H> +(\S.*)$', line)
			if not m:
				continue

			transcription = m.group(2)
			pg = str(m.group(1))

			# ignore entire line if it has a {&NNN} or {&.} code
			if re.search(r'\{&(\d|\.)+\}', transcription):
				continue

			# remove extraneous chracters ! and %
			s = transcription.replace("!", "").replace("%", "")

			# delete all end of line {comments} (between one and three observed)
			# ...with optional line terminator
			# allow 0 occurences to remove end-of-line markers (- or =)
			s = re.sub(r'([-=]?\{[^\{\}]+?\}){0,3}[-=]?\s*$', "", s)

			# delete start of line {comments} (single or double)
			s = re.sub(r'^(\{[^\{\}]+?\}){1,2}', "", s)

			# these tags are word breaks
			# breaks = [r'plant', r'figure', r'gap', r'root', r'hole', r'spray',
			# 		  r'gal', r'sync gap', r'diagram', r'star', r'blot\??', r'stem',
			# 		  r'stitched slit', r'stream', r'top of diagram', r'wide gap',
			# 		  r'\|\|', r'fold', r'crease']
			# s = re.sub(r'[-=]\{(' + r'|'.join(breaks) + r')\}', ".", s)

			# simplification: tags preceeded by -= are word breaks
			s = re.sub(r'[-=]\{[^\{\}]+?\}', '.', s)

			# these tags are nulls
			# plant is a null in one case where it is just {plant}
			# otherwise (above) it is a word break
			# s = re.sub(r'\{(fold|crease|blot|&\w.?|plant)\}', "", s)
			# simplification: remaining tags in curly brackets
			s = re.sub(r'\{[^\{\}]+?\}', '', s)

			# special case .{\} is still a word break
			s = re.sub(r'\.\{\\\}', ".", s)

			# split on word boundaries
			words = [str(w) for w in s.split(".")]

			if page_numbers:
				r = [pg]
				r.extend(words)
				yield r
			else:
				yield words

if __name__ == "__main__":
	for line in get_words("text16e6.evt"):
		print line




