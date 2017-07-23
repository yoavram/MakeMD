import re

from bibtexparser import load as load_bib
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import click

species_pattern = re.compile(
	r'({\\textless}i{\\textgreater}\w.*?{\\textless}/i{\\textgreater})'
)

@click.group()
def cli():
	pass

@cli.command()
@click.argument('markdown_filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.argument('keys_filename', type=click.Path(file_okay=True, dir_okay=False, writable=True))
def list(markdown_filename, keys_filename):
	pattern = re.compile('@([-\w]+\d{4}[a-z]?)')
	with open(markdown_filename) as f:
		groups = (pattern.findall(line) for line in f)
		groups = sum((g for g in groups if g), [])	
	groups = set(groups)
	with open(keys_filename, 'wt') as f:
		for g in groups:
			print(g, file=f)


@cli.command()
@click.argument('keys_filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.argument('bibtex_filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.argument('output_filename', type=click.Path(file_okay=True, dir_okay=False, writable=True))
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
def extract(keys_filename, bibtex_filename, output_filename, verbose):
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


if __name__ == '__main__':
	cli()