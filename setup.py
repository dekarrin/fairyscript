from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='scrappy',
	version='1.0.0',
	description='The SCRipt APplication written in PYthon, is a compiler for manuscripts.',
	long_description=long_description,
	url='https://github.com/dekarrin/scrappy',
	author='Rebecca C. Nelson',
	classifiers=[
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Topic :: Software Development :: Compilers',
		'Development Status :: 5 - Production/Stable',
	],
	keywords='renpy visual novel screenplay script word office',
	packages=['scrappy'],
	install_requires=['lxml', 'ply'],
	tests_require=[],
	python_requires='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
	entry_points={
		'console_scripts': [
			'scpcompile=scrappy:run'
		]
	}
)
