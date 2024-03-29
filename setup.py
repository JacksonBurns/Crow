import os.path
import codecs
import pathlib
from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
README = (cwd / "README.md").read_text()

setup(
    name="CrowHTE",
    version=get_version("crow/__init__.py"),
    description="Python GUI to enable High Throughput Experimentation.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JacksonBurns/Crow",
    author="Jackson Burns",
    author_email="jburnsky@udel.edu",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=read("requirements.txt").split("\n"),
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["crow=crow.__main__:start_Crow", ]},
)
