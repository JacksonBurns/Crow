
Crow - Accelerating High Throughput Experimentation
===================================================


.. image:: /Crow/other/Crow_logo.png
   :target: /Crow/other/Crow_logo.png
   :alt: Crow Logo



.. image:: https://img.shields.io/github/stars/JacksonBurns/Crow?style=social
   :target: https://img.shields.io/github/stars/JacksonBurns/Crow?style=social
   :alt: GitHub Repo stars


.. image:: https://img.shields.io/pypi/dm/CrowHTE
   :target: https://img.shields.io/pypi/dm/CrowHTE
   :alt: PyPI - Downloads


.. image:: https://img.shields.io/pypi/v/CrowHTE
   :target: https://img.shields.io/pypi/v/CrowHTE
   :alt: PyPI


.. image:: https://img.shields.io/pypi/l/CrowHTE
   :target: https://img.shields.io/pypi/l/CrowHTE
   :alt: PyPI - License


Crow is a software package for retrieving, diagnosing, and presenting High Throughput Experimentation data from various instruments. Designed by Jackson Burns at the University of Delaware Donald Watson Lab in 2019, coded in Python in 2020 and still under active development.

Installation and Setup
----------------------

Crow can be installed from the python package index (PyPi) with the following command:

``pip install CrowHTE``

Crow can then be started by typing ``crow`` in the command line.

A step-by-step setup tutorial, including how to set up a python environment and access this repository, is `available here <https://github.com/JacksonBurns/Crow/blob/main/Crow/other/setup_step-by-step.md>`_.

To configure Crow to work for your instruments, modify **config.yaml** to work for your local installation. Data is retrieved by parsing XML files output by the software on the High Throughput Experimentation instrument. For example, our setup uses an Agilent GC and their software to run experiments and calculate eluate peak areas. Again, for an in-depth setup tutorial, see `here <https://github.com/JacksonBurns/Crow/blob/main/Crow/other/setup_step-by-step.md>`_.

Using Crow
----------

Please see `this website <https://www.jacksonwarnerburns.com/crow-video-tutorials>`_ for comprehensive video tutorials detailing how to use ``Crow`` in every stage of your workflow. 

Support
-------

If you need help with setting up Crow, finding out how to retrieve data from your HTE instrument, or you find this program at all helpful, send me a message.

To contribute to project, report or a bug, or request a new feature, open a pull request using one of the provided templates.
