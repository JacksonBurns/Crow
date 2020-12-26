import pathlib
from setuptools import setup

# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
README = (cwd / "README.md").read_text()


setup(
    name="CrowHTE",
    version="1.2.0",
    description="Python GUI to enable High Throughput Experimentation.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JacksonBurns/Crow",
    author="Jackson Burns",
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=["Crow"],
    include_package_data=True
)
