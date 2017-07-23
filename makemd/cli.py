import re

from . import __version__

from bibtexparser import load as load_bib
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import click

_print = print
def print(msg, file=None):
	if file is None:
		click.secho(s, fg='red')
	else:
		_print(msg, file=file)


@click.group()
@click.version_option(version=__version__)
def cli():
	pass

@cli.command()
@click.argument('markdown_input', type=click.File('rt'))
@click.argument('keys_output', type=click.File('wt'))
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
def list(markdown_input, keys_output, verbose):
	pattern = re.compile('@([-\w]+\d{4}[a-z]?)')
	groups = (pattern.findall(line) for line in markdown_input)
	groups = sum((g for g in groups if g), [])	
	groups = set(groups)
	if verbose:		
		print("Writing {} keys from {} to {}".format(len(groups), 
			click.format_filename(markdown_input.name), click.format_filename(keys_output)))		
	for g in groups:
		print(g, file=keys_output)



@cli.command()
@click.argument('keys_input', type=click.File('rt'))
@click.argument('bibtex_input', type=click.File('r'))
@click.argument('bibtex_output', type=click.File('wt'))
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
def extract(keys_input, bibtex_input, bibtex_output, verbose):
	lines = keys_input.readlines()
	citation_keys = (line.strip() for line in lines)
	if verbose:
		print("Read {} keys from {}".format(len(lines), 
			click.format_filename(keys_input.name)))
	main_bib = load_bib(bibtex_input)
	if verbose:
		print("Read {} entries from {}".format(len(main_bib.entries), 
			click.format_filename(bibtex_input.name)))

	out_bib = BibDatabase()
	species_pattern = re.compile(
		r'({\\textless}i{\\textgreater}\w.*?{\\textless}/i{\\textgreater})'
	)
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
		print("Writing {} entries to {}".format(len(out_bib.entries), 
			click.format_filename(bibtex_output.name)))
	writer = BibTexWriter()
	bibtex_output.write(writer.write(out_bib))


if __name__ == '__main__':
	cli()