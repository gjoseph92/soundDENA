.. currentmodule:: soundDB

.. ipython:: python
   :suppress:

   import numpy as np
   import pandas as pd
   import soundDB
   np.set_printoptions(precision=4, suppress=True)
   pd.options.display.max_rows = 8
   pd.options.display.max_columns = 3

.. _overview:

===============================
What you'll use 90% of the time
===============================

Reading Data
============

The soundDB module has an attribute for each type of file it can access---for example, ``soundDB.nvspl``, ``soundDB.srcid``, and ``soundDB.metrics``. These are all instances of the class :class:`~soundDB.Accessor`. (For the full list of supported files, see :ref:`Filetype Accessors <filetypes>`.) There are several ways to use the Accessor class, but the most common are:

.. function:: soundDB.<filetype>(sites)
   
    Returns an iterator over the data for each site. The iterator yields a tuple of ``(data, unit, site, year)``, where ``data`` is usually a pandas DataFrame or Panel. :meth:`See full documentation <soundDB.Accessor.__call__>`.

    .. ipython:: python

        props = jets = 0
        denaliSites = ["DENAKAHP2010", "DENAWEBU2009", "DENAUKAH2011"]
        for srcid, unit, site, year in soundDB.srcid(denaliSites):
            jets += len( srcid[ srcid.srcID == 1.1 ] )
            props += len( srcid[ srcid.srcID == 1.2 ] )

        # Ratio of props to jets near the Denali massif:
        props / jets

    .. ###

        .. ipython:: python

            for metrics, unit, site, year in soundDB.metrics(["DENAFANG2013", "DENAKAHP2010", "DENAWEBU2009"]):
                summer_lnat = metrics.ambient.data.loc["Summer", "dBA", "Lnat", "overall"]
                hours = metrics.ambient.n.loc["Summer", "dBA"]
                print("{} {} summer L_nat: {} ({} hours)".format(year, site, summer_lnat, hours))

.. function:: soundDB.<filetype>.all(sites)

    Returns data from all the sites concatenated into a single object, typically a pandas DataFrame or Panel. :meth:`See full documentation <soundDB.Accessor.all>`.

    .. ipython:: python

        denaliSites = ["DENAKAHP2010", "DENAWEBU2009", "DENAUKAH2011"]
        srcids = soundDB.srcid.all(denaliSites)
        jets = len( srcids[ srcids.srcID == 1.1 ] )
        props = len( srcids[ srcids.srcID == 1.2 ] )

        # Ratio of props to jets near the Denali massif:
        props / jets


.. function:: soundDB.<filetype>.paths(sites)

     Returns an iterator over the paths to the data files for each site. :meth:`See full documentation <soundDB.Accessor.paths>`.

     .. ipython:: python

        denaliSites = ["DENAKAHP2010", "DENAWEBU2009", "DENAUKAH2011"]
        for path, unit, site, year in soundDB.srcid.paths(denaliSites):
            print(site, year, path)


In all cases, the parameter **sites** is an iterable of :ref:`siteID`\ s. It could be as simple as ``["DENAFANG2013", "DENACARB2013", "DENAPAIN2014"]``, but it can also be a pandas DataFrame or Series whose *index* is the :ref:`siteID`\ s you want. So most commonly, you'll use a subselection from the :attr:`~soundDB.metadata.metadata` DataFrame, like ``soundDB.metadata.query("unit == 'DENA' and type == 'grid'")``.

.. note::

    Why not always use ``.all()``? Though it's sometimes less convenient, iterating site-by-site greatly reduces memory useage, as you only need to keep around data for a single site at a time.

    Performing some operation on a site-by-site basis (like a median or count) is also a very common task. In any case where you only need values from one site at a time, using the iterator is often syntactically easier than dealing with the MultiIndex returned by ``.all()``.


Selecting Sites
===============

Using a list of :ref:`siteID` strings gets tedious---usually, you want data from sites that meet some criteria, like season, elevation, year, or park. This sort of metadata is found in the :attr:`Complete Metadata <soundDB.paths.metadata>` and :attr:`Derived Data <soundDB.paths.derivedData>` workbooks, so when you import soundDB, it loads both into a single pandas DataFrame, accessible as :attr:`soundDB.metadata <soundDB.metadata.metadata>`. You can then sub-select sites using criteria such as ``unit``, ``winter_site``, ``elevation``, etc. :attr:`soundDB.metadata <soundDB.metadata.metadata>`'s row indicies are :ref:`siteID`\ s, so you can use it as a site specifier for an :class:`~soundDB.Accessor`.

.. ipython:: python

    import soundDB
    soundDB.metadata
    soundDB.metadata.columns
    soundDB.metadata.index

Putting It Together
===================

By using a subselection of :attr:`soundDB.metadata <soundDB.metadata.metadata>` as the site specifier for an :class:`~soundDB.Accessor`, you can read the type of data you want from just certain sites that meet a criterion:

.. todo:: More explanation

.. ipython:: python
    
    highDena = soundDB.metadata.query("unit == 'DENA' and elevation > 2000 and not winter_site")
    highDena
    soundDB.srcid.all(highDena)
