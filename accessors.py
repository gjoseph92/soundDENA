from . import readers
from . import paths
import pathlib

"""
Accessor - knows where files are found in the a site's data directory structure

Takes: path to site's data directory (or a site ID string)
Yields: pandas DataFrame as read by the appropriate Reader
"""

# TODO: standard way for returning just the specificPathToData instead of the data itself (both in accessor and mapper)

def _accessor(readerFunc, pathToData):
    def accessorFunc(site, reader= readerFunc, pathsOnly= False, **kwargs):
        if isinstance(site, pathlib.Path):
            dataDir = site
            unit, site, year, _ = paths.splitDataDir(dataDir)
        else:
            unit, site, year = paths.splitSiteID(site)
            dataDir = paths.getDataDirPath(unit, site, year)

        specificPathToData = str(pathToData).format(unit= unit, site= site, year= year)
        pathForReader = dataDir / pathlib.Path(specificPathToData)

        if not pathForReader.exists():
            raise IOError("{} does not exist.".format(pathForReader))

        if pathsOnly:
            return pathForReader
        else:
            data = reader(pathForReader, **kwargs)
            # TODO: possibility for readerFunc to also be a generator
            return data

    return accessorFunc


nvspl      = _accessor(readers.nvspl, paths.nvspl)

srcid      = _accessor(readers.srcid, paths.spl / "SRCID_{unit}{site}.txt")
loudEvents = _accessor(readers.loudEvents, paths.spl / "LOUDEVENTS_{unit}{site}.txt")
audability = _accessor(readers.audability, paths.wav)
dailyPA    = _accessor(readers.dailyPA, paths.spl / "DAILYPA_{unit}{site}.txt")
metrics = _accessor(readers.metrics, paths.spl / "METRICS_{unit}{site}.txt")
