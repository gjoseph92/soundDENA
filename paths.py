import pathlib
import re
import pandas

###############
#### PATHS ####
###############

############
### Metadata

sound = pathlib.Path("T:/ResMgmt/WAGS/Sound")
analysis = sound / 'Analysis'

derivedData = analysis / 'DENA Parkwide Derived Data 2015 08 12 T.xls'
metadata = analysis / 'Complete_Metadata_AKR_2006-2015  T.xlsx'

############
### Raw data

rawdata = pathlib.Path("E:/AKRO Soundscape Data")

# Each raw data folder's structure:

data     = pathlib.Path( "01 DATA" )

nvspl    = data / "NVSPL"
audio    = data / "AUDIO"
photos   = data / "PHOTOS"
partial_nvspl = data / "PartialDays_NVSPL"

analysis = pathlib.Path( "02 ANALYSIS" )

spl      = analysis / "SPL Analysis"
wav      = analysis / "WAV Analysis"
computed = analysis / "Computational Outputs"

microarray = wav / "Microarray"

#################
#### METHODS ####
#################

_siteID_regex = re.compile(r"^([\w\d]{4})([\w\d]{4})(\d{4})$")
_dataDir_regex = re.compile(r"^(\d{4}) ([\w\d]{4})([\w\d]{4}) (.*)")

def splitSiteID(siteID):
    """
    Returns a 3-tuple of unit, site, and year for a site ID.
    Site IDs are formatted as UNITSITEYEAR, i.e. DENAUPST2015
    """
    match = _siteID_regex.match(siteID)
    if match:
        return match.groups()
    else:
        raise ValueError("Invalid site ID: '{}'".format(siteID))
def siteID(unit, site, year):
    """
    Formats unit, site, and year into a site ID (UNITSITEYEAR, i.e. DENAUPST2015)
    """
    return unit+site+year

def splitDataDir(dataDir):
    """
    Returns a 4-tuple of unit, site, year, and title for a data directory (pathlib.Path, or string).
    Data directory names are formatted as: YEAR UNITSITE <title>, i.e. 2014 GAARNWAL North Walker Lake
    """
    dataDir = pathlib.Path(dataDir)
    match = _dataDir_regex.match(dataDir.stem)
    if match:
        year, unit, site, title = match.groups()
        return (unit, site, year, title)
    else:
        raise ValueError("Invalid data dir name: '{}'".format(dataDir))
def dataDir(unit, site, year, title= ''):
    """
    Formats unit, site, year, and title into the name of a data directory (i.e. 2014 DENABACK Backside Lake)
    """
    return "{} {}{} {}".format(year, unit, site, title)

## Make lookup dict of all data dirs immediately upon import
_allDataDirs = {}
def _buildDataDirLookup(newRawData= None):
    global rawdata
    if newRawData is not None:
        rawdata = pathlib.Path(newRawData)
    try:
        for dataDir in rawdata.iterdir():
            try:
                unit, site, year, title = splitDataDir(dataDir)
                _allDataDirs[(unit, site, year)] = dataDir
            except ValueError:
                continue
        if len(_allDataDirs) == 0:
            import warnings
            warnings.warn("No site data directories found in {}. Check if this is really the correct path to the raw data directory.".format(str(rawdata)))
    except FileNotFoundError:
        import warnings
        warnings.warn('Raw data directory "{}" not found (the drive may be disconnected). Most data-accessing functions will raise exceptions.'.format(str(rawdata)))
    except PermissionError:
        import warnings
        warnings.warn('Permission denied to access data directory "{}". Most data-accessing functions will raise exceptions.'.format(str(rawdata)))
_buildDataDirLookup()

def getDataDirPath(*args):
    """
    Given a site ID string, or unit, site, and year, returns a pathlib.Path to
    that site's data directory.

    Raises ValueError for invalid site identifiers, or IOError for non-existent sites.
    """
    if len(args) == 1:
        # site ID string
        split = splitSiteID(args[0])
    elif len(args) == 3:
        # unit, site, year
        split = args
    else:
        raise TypeError("getDataDirPath() takes either a site ID string or unit, site, year - got {} arguments".format(len(args)))

    try:
        return _allDataDirs[split]
    except KeyError:
        raise IOError("No data directory found for {}{} in {}".format(*split))

def dataDirs(sites, quiet= True):
    """
    Generator that returns paths to raw data directories corresponding to the given sites.

    Sites can be a pandas DataFrame, in which case its index is used as the site IDs.
    Otherwise, an iterable or singleton string of site ID(s) also works.

    Yields a tuple of (pathlib.Path, unit, site, year) for the directories that contian raw data for the sites.
    """
    if isinstance(sites, pandas.core.frame.DataFrame):
        ## If given a dataframe, use its index as site ids
        siteIDs = sites.index
    elif isinstance(sites, str):
        ## Singleton strings (just one site) can be used too
        siteIDs = [sites]
    else:
        siteIDs = sites

    ## Check format of siteIDs (UNITSITEYEAR)
    splitIDs = []
    invalidIDs = []
    for siteID in siteIDs:
        try:
            split = splitSiteID(siteID)
            splitIDs.append(split)
        except ValueError:
            invalidIDs.append(siteID)

    if not quiet and len(invalidIDs) > 0: print("Invalid site IDs given: {}".format(invalidIDs))
    ## Yield corresponding directories
    for unit, site, year in splitIDs:
        try:
            dataDir = _allDataDirs[(unit, site, year)]
            yield dataDir, unit, site, year
        except KeyError:
            if not quiet: print( "No data available on the raw data drive for {}{} in {}, skipping".format(unit, site, year) )
