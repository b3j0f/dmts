Description
===========

Development management tool synchronizer.

.. image:: https://img.shields.io/pypi/l/b3j0f.dmts.svg
   :target: https://pypi.python.org/pypi/b3j0f.dmts/
   :alt: License

.. image:: https://img.shields.io/pypi/status/b3j0f.dmts.svg
   :target: https://pypi.python.org/pypi/b3j0f.dmts/
   :alt: Development Status

.. image:: https://img.shields.io/pypi/v/b3j0f.dmts.svg
   :target: https://pypi.python.org/pypi/b3j0f.dmts/
   :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/b3j0f.dmts.svg
   :target: https://pypi.python.org/pypi/b3j0f.dmts/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/implementation/b3j0f.dmts.svg
   :target: https://pypi.python.org/pypi/b3j0f.dmts/
   :alt: Supported Python implementations

.. image:: https://img.shields.io/pypi/wheel/b3j0f.dmts.svg
   :target: https://travis-ci.org/b3j0f/dmts
   :alt: Download format

.. image:: https://travis-ci.org/b3j0f/dmts.svg?branch=master
   :target: https://travis-ci.org/b3j0f/dmts
   :alt: Build status

.. image:: https://coveralls.io/repos/b3j0f/dmts/badge.png
   :target: https://coveralls.io/r/b3j0f/dmts
   :alt: Code test coverage

.. image:: https://img.shields.io/pypi/dm/b3j0f.dmts.svg
   :target: https://pypi.python.org/pypi/b3j0f.dmts/
   :alt: Downloads

.. image:: https://readthedocs.org/projects/b3j0fdmts/badge/?version=master
   :target: https://readthedocs.org/projects/b3j0fdmts/?badge=master
   :alt: Documentation Status

.. image:: https://landscape.io/github/b3j0f/dmts/master/landscape.svg?style=flat
   :target: https://landscape.io/github/b3j0f/dmts/master
   :alt: Code Health

Links
=====

- `Homepage`_
- `PyPI`_
- `Documentation`_

Installation
============

pip install b3j0f.dmts

Features
========

The development management tool synchronizer (DMTS) consists to synchronize data from such tools (thanks to the b3j0f sync system `b3j0f.sync`_).

In this implementation, we use these models:

- Project (b3j0f.dmts.model.item.project).
- Issue (b3j0f.dmts.model.item.issue).
- Account (b3j0f.dmts.model.account).
- Comment (b3j0f.dmts.model.comment).
- Group (b3j0f.dmts.model.group).
- Label (b3j0f.dmts.model.label).
- Member (b3j0f.dmts.model.member).
- Milestone (b3j0f.dmts.model.milestone).

And this store:

- RESTStore (b3j0f.dmts.rest).

This project is also an example of data synchronizing between jira, gitlab and github.

And these examples of stores:

- Jira (b3j0f.dmts.jira).
- Github (b3j0f.dmts.github).
- Gitlab (b3j0f.dmts.gitlab).

Perspectives
============

- wait feedbacks during 6 months before passing it to a stable version.
- Cython implementation.

Donation
========

.. image:: https://cdn.rawgit.com/gratipay/gratipay-badge/2.3.0/dist/gratipay.png
   :target: https://gratipay.com/b3j0f/
   :alt: I'm grateful for gifts, but don't have a specific funding goal.

.. _Homepage: https://github.com/b3j0f/dmts
.. _Documentation: http://b3j0fdmts.readthedocs.org/en/master/
.. _PyPI: https://pypi.python.org/pypi/b3j0f.dmts/

.. _b3j0f.sync: https://github.com/b3j0f/sync
