import re

from bibtexparser import load as load_bib
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


species_pattern = re.compile(
	r'({\\textless}i{\\textgreater}\w.*?{\\textless}/i{\\textgreater})'
)

def bibtex(keys_filename, bibtex_filename, output_filename, verbose):
	with open(keys_filename) as f:
		citation_keys = (line.strip() for line in f.readlines())
	if verbose:
		print("Read {} keys from {}".format(len(citation_keys), citation_keys))

	with open(bibtex_filename) as f:
		main_bib = load_bib(f)
	if verbose:
		print("Read {} entries from {}".format(len(main_bib.entries), bibtex_filename))

	out_bib = BibDatabase()
	for key in citation_keys:
		e = main_bib.entries_dict[key]		
		title = e['title']
		groups = species_pattern.findall(title)
		for grp in groups:
			s = grp.replace(
				'{\\textless}i{\\textgreater}', ''
			).replace(
				'{\\textless}/i{\\textgreater}', ''
			)
			s = '\\textit{\\uppercase{' + s[0] + '}' + s[1:] + '}'
			title = title.replace(grp, s)
		e['title'] = title		
		out_bib.entries.append(e)
	if verbose:
		print("Writing {} entries to {}".format(len(out_bib.entries), output_filename))
	writer = BibTexWriter()
	with open(output_filename, 'w') as f:
	    f.write(writer.write(out_bib))
