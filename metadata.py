import pandas as pd
import numpy as np
import pathlib

from . import paths

def fullMetadata():
    """
    Returns a DataFrame of metadata merged with derived data, with overlapping
    columns resolved, and all column names in lowercase.
    The DataFrame is indexed by site id: the 12-character code of UNITSITEYEAR, i.e. DENAUPST2015.

    TODO: save the result, and recompute it only when its date modified is older than the
          date modified of metadata or derived data
    """
    derivedData = pd.read_excel(str(paths.derivedData))
    metadata = pd.read_excel(str(paths.metadata))
    derivedData.columns = derivedData.columns.str.lower()
    derivedData.rename(columns= {"park": "unit", "code": "site", "site": "title"}, inplace= True)
    metadata.rename(columns= {"code": "site", "site": "title"}, inplace= True)

    # Strip whitespace from string columns
    for df in [metadata, derivedData]:
        stringCols = df.dtypes[ df.dtypes == np.object ].index
        df[stringCols] = df[stringCols].apply(lambda col: col.str.strip())

    full = pd.merge(metadata, derivedData, on=['unit', 'site', 'year'], suffixes= ("_meta", "_derived"))
    
    dupCols = derivedData.columns.intersection(metadata.columns).difference(['unit', 'site', 'year'])
    for col in dupCols:
        full[col+"_meta"].replace(to_replace= np.nan, value= full[col+"_derived"], inplace= True)
        full.rename(columns= {col+"_meta": col}, inplace= True)
        full.drop(col+"_derived", axis= 1)

    ids = full.apply(lambda site: paths.siteID(site.unit, site.site, site.year), axis= 1)
    full.index = ids
    full.winter_site = full.winter_site.astype(bool)

    return full

metadata = fullMetadata()
