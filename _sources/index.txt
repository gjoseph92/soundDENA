.. soundDB documentation master file, created by
   sphinx-quickstart on Wed Sep 23 13:24:06 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. ipython:: python
   :suppress:

   import numpy as np
   import pandas as pd
   np.set_printoptions(precision=4, suppress=True)
   pd.options.display.max_rows = 8
   pd.options.display.max_columns = 3

.. _intro:

soundDB
=======

soundDB is a Python library for easily and precisely accessing various sorts of natural sounds data in bulk. It allows you to treat the NSNSD hierarchical file structure almost as though it were a queryable database.

SoundDB:

    * Provides accessor methods which handle and normalize inconsistencies in naming and file formats: input data may differ, but the output is consistent
    * Associates metadata with data, so data can be selected based on a query of its metadata
    * Returns data in `pandas <http://pandas.pydata.org/>`_ structures, which excel at concise and efficient subselection, querying, aggregation, and general wrangling
    * Plays nicely with the Python scientific computing ecosystem
    * Handles missing data without making a fuss

A taste of soundDB:

.. ipython:: python

    import soundDB
    query = 'unit == "DENA" and type == "Grid" and not winter_site'
    denaSummerGrid = soundDB.metadata.query(query)
    srcids = soundDB.srcid.all(denaSummerGrid)
    srcids
    # Total length of noise events, by vehicle type:
    srcids.groupby("srcID")["len"].sum()

Contents:

.. toctree::
   :maxdepth: 2

   overview
   accessor
   filetypes
   paths
   metadata


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

