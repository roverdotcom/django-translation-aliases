========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/django-translation-aliases/badge/?style=flat
    :target: https://readthedocs.org/projects/django-translation-aliases
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/roverdotcom/django-translation-aliases.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/roverdotcom/django-translation-aliases

.. |codecov| image:: https://codecov.io/github/roverdotcom/django-translation-aliases/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/roverdotcom/django-translation-aliases

.. |version| image:: https://img.shields.io/pypi/v/django-translation-aliases.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/django-translation-aliases

.. |commits-since| image:: https://img.shields.io/github/commits-since/roverdotcom/django-translation-aliases/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/roverdotcom/django-translation-aliases/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-translation-aliases.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/django-translation-aliases

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/django-translation-aliases.svg
    :alt: Supported versions
    :target: https://pypi.org/project/django-translation-aliases

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/django-translation-aliases.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/django-translation-aliases


.. end-badges

A small library which adds "translate" and "blocktranslate" templatetags as and modified makemessages to work with
them.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install django-translation-aliases

Documentation
=============


https://django-translation-aliases.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
