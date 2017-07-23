from setuptools import setup, find_packages
from codecs import open
from os import path

import versioneer
__version__ = versioneer.get_version()

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read()
    all_reqs = all_reqs[:all_reqs.index('# Dev')]
    all_reqs = all_reqs.split('\n')
install_requires = [x.strip() for x in all_reqs if 'git+' not in x and x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='makemd',
    version=__version__,
    cmdclass=versioneer.get_cmdclass(),
    description='Assisting the production of PDF files from Markdown with Pandoc',
    long_description=long_description,
    url='https://github.com/yoavram/makemd',
    download_url='https://github.com/yoavram/makemd/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Yoav Ram',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='yoav@yoavram.com',
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'makemd=makemd.cli:cli',
        ],
    },
)
