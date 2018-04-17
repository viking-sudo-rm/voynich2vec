#!/usr/bin/env python3

# TODO:
# 89r2 paragraph issue
# weirdo characters
# column breaks

from collections import Counter
import re

wordCounter = Counter()

with open("text16e6.evt", 'r', encoding="latin_1") as file:
	for line in file.read().splitlines():
		# pull out takahashi lines
		m = re.match(r'^<f.*;H> +(\S.*)$', line)
		if not m:
			continue

		transcription = m.group(1)

		# remove extraneous chracters ! and %
		s = transcription.translate(str.maketrans("","","!%"))

		# delete all end of line {comments} (between one and three observed)
		# ...with optional line terminator
		s = re.sub(r'([-=]?\{[^\{\}]+?\}){1,3}[-=]?$', "", s)

		# delete start of line {comments} (single or double)
		s = re.sub(r'^(\{[^\{\}]+?\}){1,2}', "", s)

		# these tags are word breaks
		s = re.sub(r'[-=]\{(plant|figure|gap|root|hole|spray|gal|sync gap|diagram)\}', ".", s)

		# these tags are nulls
		s = re.sub(r'\{(fold|crease)\}', "", s)

		# if "{" in s:
		print(s)

		# split on word boundaries or illustrations (/ other annotations)
		#words = re.split(r'\.|-?\{.+\}', line)

		#print(words)
		
		#wordCounter.update(w.translate(str.maketrans("",""," -=!%")) for w in filter(None, words))

#print(len(wordCounter))

# s = 0

# for i, w in enumerate(wordCounter.most_common()):
# 	print(w)
# 	s += w[1]

#print(s)
