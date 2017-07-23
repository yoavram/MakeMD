import re

import click

@click.command()
@click.argument('markdown_filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.argument('keys_filename', type=click.Path(file_okay=True, dir_okay=False, writable=True))
def main(markdown_filename, keys_filename):
	pattern = re.compile('@([-\w]+\d{4}[a-z]?)')
	with open(markdown_filename) as f:
		groups = (pattern.findall(line) for line in f)
		groups = sum((g for g in groups if g), [])	
	groups = set(groups)
	with open(keys_filename, 'wt') as f:
		for g in groups:
			print(g, file=f)

if __name__ == '__main__':
	main()