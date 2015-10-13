import pandas as pd
import numpy as np
import pathlib

from . import paths


# TODO: save the result, and recompute it only when its date modified is older than the
# date modified of metadata or derived data
def fullMetadata():
    """
    Returns a DataFrame of metadata merged with derived data, with overlapping
    columns resolved. Some column names and values are changed for consistency.

    Transformations:

        * ``unit`` column refers to ``Park`` from Derived Data and ``unit`` from Metadata
        * ``code`` column is renamed to ``site`` (the 4-character site code)
        * ``site`` column is renamed to ``title``
        * All column names are lowercased
        * In overlapping columns, values from Metadata are used
          where values from both Metadata and Derived Data exist
        * Leading and trailing whitespace is stripped from all string values
        * Columns that contain only the values 0 and 1 are assumed to be boolean,
          and converted to a boolean datatype

    Returns
    -------
    DataFrame
        Indexed by siteID (the 12-character code of UNITSITEYEAR, i.e. DENAUPST2015)
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

    full = pd.merge(metadata, derivedData, on=['unit', 'site', 'year'], how= "outer", suffixes= ("_meta", "_derived"))
    
    # Resolve overlapping columns, tie goes to metadata
    dupCols = derivedData.columns.intersection(metadata.columns).difference(['unit', 'site', 'year'])
    for col in dupCols:
        full[col+"_meta"].replace(to_replace= np.nan, value= full[col+"_derived"], inplace= True)
        full.rename(columns= {col+"_meta": col}, inplace= True)
        full.drop(col+"_derived", axis= 1)

    # Set index to siteIDs
    ids = full.apply(lambda site: paths.siteID(site.unit, site.site, site.year), axis= 1)
    full.index = ids

    # Convert boolean-looking columns to boolean datatype
    for col in full:
        unique = full[col].unique()
        if len(unique) <= 3:
            unique = set( unique[ ~pd.isnull(unique) ] )
            if unique == {1, 0}:
                full[col] = full[col].astype(bool)

    # full.winter_site = full.winter_site.astype(bool)

    return full

metadata = fullMetadata()
