.. currentmodule:: soundDENA

.. _accessor:

==================
The Accessor Class
==================

For every type of file, where it's found in the NSNSD file hierarchy and how it's parsed is different. However, once you know the where and how, the logic for reading *many* of those types of files from multiple sites is the same. The Accessor class provides this generalization: given a function for reading a datatype from a single site, each instance provides methods for applying that function to multiple sites.

Example: creating an accessor for RAVEN data::

    import soundDENA
    import pandas as pd

    def parseRAVENfile(pathToFile):
        data = pd.read_table(pathToFile)
        data.rename(columns= {"Species_"+i: "Species "+i for i in "1234"}, inplace= True)
        return data

    pathToRAVENfileWithinSite = "02 ANALYSIS/RAVEN/table_{unit}{site}.txt"

    ravenAccessor = soundDENA.Accessor(parseRAVENfile,
                                     pathToRAVENfileWithinSite)

    ## You can now do things like:
    
    ravenAccessor.all(["DENAFANG2013", "DENAWEBU2009"])
    ## Returns a DataFrame of RAVEN data for both the sites

    for data, unit, site, year in ravenAccessor(soundDENA.metadata.query("elevation < 500")):
        unique = sum(data["Species "+i].nunique() for i in "1234")
        print("{} in {}: {} unique species".format(site, year, unique))

.. autoclass:: Accessor
    :members:
    :special-members:
    :exclude-members: __weakref__
