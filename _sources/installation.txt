.. _installation:

============
Installation
============

soundDENA is hosted as a Python wheel here on GitHub, so it can be installed using the package manager ``pip``.

.. important::

	Currently, soundDENA is **Denali-specific**. So unless your name is Davy-d H Betchkal, you have little reason to be following these instructions. If you want to try it on your own data, you'll need to clone the `GitHub repository <https://github.com/gjoseph92/soundDENA>`_ and tinker with the constants in :ref:`soundDENA.paths <paths>` on your own.

Dependencies:
=============

	* Python 3.4 or greater. On Windows, you'll almost certainly want to use the `Anaconda distribution <https://www.continuum.io/downloads#_windows>`_.
	* `SciPy <http://www.scipy.org/>`_:
		* `Numpy <http://www.numpy.org/>`_ 1.9 or greater.
		* `Pandas <http://pandas.pydata.org/>`_ 0.16.x. (Currently, 0.17 may break things and has not yet been tested.)
		* On Windows, Anaconda is by far the easiest way to install these (and most other) packages. Be sure to have them installed *before* using pip, as pip will try to install numpy and pandas on its own if it finds them missing, which will not go well.

Installing & Upgrading:
=======================

Windows
-------

Open Command Prompt and enter this command::

	pip install --upgrade --no-deps --index-url https://gjoseph92.github.io/soundDENA/dist/ soundDENA

The ``--upgrade`` will upgrade soundDENA to the latest version, even if it's already installed.

``--no-deps`` (no dependencies) is important on Windows, as otherwise pip might try to upgrade numpy and scipy at the same time, but those packages should only be upgraded by Anaconda.

Linux/Mac
---------

This command in a shell will work::

	pip install --upgrade --index-url https://gjoseph92.github.io/soundDENA/dist/ soundDENA
