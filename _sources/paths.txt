.. currentmodule:: soundDENA

.. _paths:

==========================
Path & Directory Structure
==========================

soundDENA relies on the regularity of the NSNSD file structure and naming scheme to be able to locate file types across multiple sites. In order to be easily reconfigurable to future changes or different systems, however, the expected layout of this file structure is defined in just one place: the ``paths`` submodule. ``soundDENA.paths`` defines many constants that specify where different directories can be found, as well as functions for mapping between site identifiers. Because the rest of the library only uses these methods and constants, never assuming the format of names or folders, adapting to a new naming convention only requires modifying simple code in this file.

Terms & Formats
===============

+---------+---------------------------+---------------------------------+--------------------------------------------------------+
|  Term   |        Format             |      Example                    |                Description                             |
+=========+===========================+=================================+========================================================+
| unit    | ``AAAA``                  |          ``DENA``               | Four-character alphanumeric code for the unit (park)   |
|         |                           |                                 | of the site                                            |
+---------+---------------------------+---------------------------------+-------------------+------------------------------------+
| site    | ``AAAA``                  |           ``FANG``              | Four-character alphanumeric code for the site itself   |
+---------+---------------------------+---------------------------------+-------------------+------------------------------------+
| year    | ``9999``                  |           ``2013``              | Four-character numeric code for the year of            |
|         |                           |                                 | sampling of the site                                   |
+---------+---------------------------+---------------------------------+-------------------+------------------------------------+
| siteID  | ``UNITSITEYEAR``          |       ``DENAFANG2013``          | A string identifier for a unique sampling of data.     |
|         |                           |                                 | siteID is used throughout soundDENA as the standard way  |
|         |                           |                                 | to identify and refer to a site across many contexts.  |
+---------+---------------------------+---------------------------------+-------------------+------------------------------------+
| dataDir | ``YEAR UNITSITE <title>`` | ``2013 DENAFANG Fang Mountain`` | The root directory containing raw and analyzed         |
|         |                           |                                 | data for a particular site                             |
+---------+---------------------------+---------------------------------+-------------------+------------------------------------+

Name-Formatting Methods
=======================

.. automodule:: soundDENA.paths
   :members:
   :undoc-members:

Base Absolute Locations
=======================

.. currentmodule:: soundDENA.paths

.. autodata:: t_analysis
.. autodata:: derivedData
.. autodata:: metadata
.. autodata:: rawdata

Directory Structure Constants
=============================

.. autodata:: data
.. autodata:: nvspl
.. autodata:: audio
.. autodata:: photos
.. autodata:: partial_nvspl
.. autodata:: analysis
.. autodata:: spl
.. autodata:: wav
.. autodata:: computed
.. autodata:: microarray
