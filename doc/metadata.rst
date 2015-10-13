.. currentmodule:: soundDB

.. _metadata:

========
Metadata
========

The metadata about each site is typically the entry point for soundDB data access, as it's queried to identify from which sites data should be read. The :attr:`Complete Metadata <soundDB.paths.metadata>` and :attr:`Derived Data <soundDB.paths.derivedData>` Excel workbooks are joined into one DataFrame when soundDB is imported.

.. data:: soundDB.metadata

	A DataFrame of the Complete Metadata and Derived Data workbooks. Indexed by ``siteID``, with the union of all columns in both those workbooks. The column names and data are slightly modified for consistency; see :func:`~soundDB.fullMetadata` for specifics.

Though unlikely, if these workbooks ever change midway through a script or interactive session, you can reload them using:

.. autofunction:: soundDB.fullMetadata

