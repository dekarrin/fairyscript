from setuptools import setup, find_packages
from os import path
import codecs
import re


def read(*parts):
	here = path.abspath(path.dirname(__file__))
	with codecs.open(path.join(here, *parts), 'r') as fp:
		return fp.read()


def find_version():
	version_file = read("scrappy", "__init__.py")
	version_match = re.search(r"^\s*__version__\s*=\s*['\"]([^'\"]*)['\"]\s*$", version_file, re.MULTILINE)

	if version_match:
		return version_match.group(1)
	else:
		raise RuntimeError("Unable to find version string")


setup(
	name='scrappy',
	version=find_version(),
	description='The SCRipt APplication written in PYthon, is a compiler for manuscripts.',
	long_description=read('README.md'),
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
	packages=find_packages(),
	install_requires=['lxml', 'ply'],
	tests_require=[],
	python_requires='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
	entry_points={
		'console_scripts': [
			'scpcompile=scrappy:run'
		]
	},
	package_data={
		'': ['docx/templates/*.docx', 'docx/templates/*.xml']
	},
	include_package_data=True
)
