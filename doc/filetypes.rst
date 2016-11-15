.. currentmodule:: soundDENA

.. _filetypes:

===========================
Filetype-Specific Accessors
===========================

soundDENA includes Accessor instances for the following filetypes. (They're available as ``soundDENA.<filetype>``, i.e. ``soundDENA.nvspl(sites)``, ``soundDENA.srcid.all(sites)``, etc.) This page lists the documentation for each of their :meth:`~soundDENA.Accessor.parse` methods---how they behave on data from a single site. This behavior is then applied to multiple sites using :meth:`~soundDENA.Accessor.__call__`, or concatenated using :meth:`~soundDENA.Accessor.all`.

.. important::

    Remember, you will be using these wrapped up in instances of :class:`soundDENA.Accessor`. Though this page implies that ``soundDENA.nvspl`` returns a DataFrame, ``soundDENA.nvspl(sites)`` is actually an iterator, which yields such a DataFrame for every site.

.. autodata:: soundDENA.nvspl
    :annotation:

.. autodata:: soundDENA.srcid
    :annotation:

.. autodata:: soundDENA.loudevents
    :annotation:

.. autodata:: soundDENA.dailypa
    :annotation:

.. autodata:: soundDENA.metrics
    :annotation:

