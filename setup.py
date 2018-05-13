from setuptools import setup, find_packages
from os import path
import codecs
import re


def read(*parts):
	here = path.abspath(path.dirname(__file__))
	with codecs.open(path.join(here, *parts), 'r') as fp:
		return fp.read()


def find_version():
	version_file = read("fairyscript", "__init__.py")
	version_match = re.search(r"^\s*__version__\s*=\s*['\"]([^'\"]*)['\"]\s*$", version_file, re.MULTILINE)

	if version_match:
		return version_match.group(1)
	else:
		raise RuntimeError("Unable to find version string")


setup(
	name='fairyscript',
	version=find_version(),
	description='FairyScript is a language for compiling manuscripts.',
	long_description=read('README.md'),
	url='https://github.com/dekarrin/fairyscript',
	author='Rebecca Nelson',
	author_email='dekarrin.irl@gmail.com',
	classifiers=[
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
	python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
	entry_points={
		'console_scripts': [
			'fairyc=fairyscript:run'
		]
	},
	package_data={
		'': ['docx/templates/*.docx', 'docx/templates/*.xml']
	},
	include_package_data=True
)
