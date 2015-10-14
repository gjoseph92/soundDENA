.. currentmodule:: soundDB

.. _filetypes:

===========================
Filetype-Specific Accessors
===========================

soundDB includes Accessor instances for the following filetypes. (They're available as ``soundDB.<filetype>``, i.e. ``soundDB.nvspl(sites)``, ``soundDB.srcid.all(sites)``, etc.) This page lists the documentation for each of their :meth:`~soundDB.Accessor.parse` methods---how they behave on data from a single site. This behavior is then applied to multiple sites using :meth:`~soundDB.Accessor.__call__`, or concatenated using :meth:`~soundDB.Accessor.all`.

.. important::

    Remember, you will be using these wrapped up in instances of :class:`soundDB.Accessor`. Though this page implies that ``soundDB.nvspl`` returns a DataFrame, ``soundDB.nvspl(sites)`` is actually an iterator, which yields such a DataFrame for every site.

.. autodata:: soundDB.nvspl
    :annotation:

.. autodata:: soundDB.srcid
    :annotation:

.. autodata:: soundDB.loudevents
    :annotation:

.. autodata:: soundDB.dailypa
    :annotation:

.. autodata:: soundDB.metrics
    :annotation:

