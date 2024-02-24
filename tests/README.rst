..
  SPDX-FileCopyrightText: KB Sriram
  SPDX-License-Identifier: MIT
..

Itertools Tests
===============

These tests run under CPython, and are intended to verify that the
Adafruit library functions return the same outputs compared to ones in
the standard `itertools` module, and also to exercise some type
annotations.

These tests run automatically from the standard `circuitpython github
workflow <wf_>`_. To run them manually, first install these packages
if necessary::

  $ pip3 install pytest

Then ensure you're in the *root* directory of the repository and run
the following command::

  $ python -m pytest

Type annotation tests don't run automatically at this point. But to
verify type-related issues manually, first install these packages if
necessary::

  $ pip3 install mypy

Then ensure you're in the *root* directory of the repository and run
the following command::

  $ mypy --warn-unused-ignores --disallow-untyped-defs tests


.. _wf: https://github.com/adafruit/workflows-circuitpython-libs/blob/6e1562eaabced4db1bd91173b698b1cc1dfd35ab/build/action.yml#L78-L84
