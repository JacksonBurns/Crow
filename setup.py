import pathlib
from setuptools import setup, find_packages

# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
README = (cwd / "README.md").read_text()

setup(
    name="CrowHTE",
    version="1.3.0",
    description="Python GUI to enable High Throughput Experimentation.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JacksonBurns/Crow",
    author="Jackson Burns",
    author_email="jburnsky@udel.edu",
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "six",
        "kiwisolver>=1.0.1",
        "python-dateutil>=2.1",
        "cycler>=0.10",
        "pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.3",
        "pillow",
        "matplotlib>=3.1.3",
        "pyyaml",
        "numpy",
        "setuptools"
    ],
    packages=['Crow','Crow.Crow_GC','Crow.helper_functions','Crow.test','Crow.other'],
    include_package_data=True,
    entry_points={
    'console_scripts': [
        'crow=Crow.Crow:main',
    ]
    }
)
