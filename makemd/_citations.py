import re

def citations(markdown_filename, keys_filename):
	pattern = re.compile('@([-\w]+\d{4}[a-z]?)')
	with open(markdown_filename) as f:
		groups = (pattern.findall(line) for line in f)
		groups = sum((g for g in groups if g), [])	
	groups = set(groups)
	with open(keys_filename, 'wt') as f:
		for g in groups:
			print(g, file=f)
