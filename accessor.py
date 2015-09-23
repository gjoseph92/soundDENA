from . import paths

import pandas as pd
import pathlib
import glob
import traceback

class Accessor:
    pathToData = None

    @classmethod
    def __init__(cls):
        cls.__doc__ = cls.parse.__doc__

    @classmethod
    def __call__(cls, sites, quiet= True, **kwargs):
        """
        Iterate site-by-site over a type of data.

        Takes: an iterable of sites (typically a DataFrame indexed by site ID)
        Yields: tuple of
                0 - data for each site of whatever kind of data you asked for,
                    as read by the appropriate Reader
                1 - unit
                2 - site
                3 - year
        """
        for dataDir, unit, site, year in paths.dataDirs(sites, quiet= quiet):
            try:
                data = cls.access((dataDir, unit, site, year), **kwargs)
                yield data, unit, site, year
            except OSError as e:
                if not quiet: print( e )
            except:
                # TODO: clearer error handling
                # print( _sys.exc_info()[0] )
                if not quiet: print( "Error when processing {}:".format(dataDir) )
                if not quiet: print( traceback.format_exc() )
                continue

    @classmethod
    def all(cls, sites, quiet= True, **kwargs):
        """
        Read data from all specified sites.

        If the parser retuns a pandas NDFrame, all sites will be concatenated into
        one concatenated dataframe, with siteID as outermost level of hierarchical index.

        Otherwise, return a dict of { siteID: data }
        """
        results = { paths.siteID(unit, site, year): data for data, unit, site, year in cls.__call__(sites, quiet= quiet, **kwargs) }
        try:
            joined = pd.concat(results)
            try:
                joined.index.set_names('siteID', level= 0, inplace= True)
            except AttributeError:
                pass
            return joined

            # TODO: do a better job than concat by promoting to next-dimensionality data structure
        except TypeError:
            return results

    @classmethod
    def paths(cls, sites):
        """
        Iterate site-by-site over the paths to this sort of data file.

        Yields a pathlib.Path, or possibly a list of pathlib.Path.
        """
        for dataDir, unit, site, year in paths.dataDirs(sites):
            try:
                yield cls._filepath(dataDir, unit, site, year), unit, site, year
            except OSError:
                continue

    @classmethod
    def access(cls, site, **kwargs):
        """
        Read data from one site, specified by siteID, data directory, (unit, site, year), or (dataDir, unit, site, year)
        """
        if isinstance(site, tuple) or isinstance(site, list):
            if len(site) == 4:
                dataDir, unit, site, year = site
            elif len(site) == 3:
                unit, site, year = site
                dataDir = paths.getDataDirPath(unit, site, year)
            else:
                raise ValueError("Wrong tuple length for site specification {}: if a tuple, site should be (unit, site, year), or (dataDir, unit, site, year)".format(site))      
        elif isinstance(site, pathlib.Path):
            dataDir = site
            unit, site, year, _ = paths.splitDataDir(dataDir)
        elif isinstance(site, str):
            unit, site, year = paths.splitSiteID(site)
            dataDir = paths.getDataDirPath(unit, site, year)
        else:
            raise ValueError("Unknown site specification {}".format(site))

        filePath = cls._filepath(dataDir, unit, site, year)
        return cls.parse(filePath, **kwargs)

    @staticmethod
    def parse(filepath, **kwargs):
        raise NotImplementedError
    
    @classmethod
    def _filepath(cls, dataDir, unit, site, year):
        """
        Return the path (or list of paths) to the data file(s) for the given site of this type,
        by filling in `cls.pathToData`.

        In the default implementation, cls.pathToData can be a pathlib.Path that looks like a
        Python format string, i.e. `paths.spl / "SRCID_{unit}{site}.txt"`. It is formatted with keyword
        arguments for unit, site, and year, and joined onto the root data directory for the site. If
        the path contains a `*` character, it will be passed to `glob`, and the resulting list will
        be converted to pathlib.Paths and returned.
        """
        specificPathToData = str(cls.pathToData).format(unit= unit, site= site, year= year)
        pathForReader = dataDir / pathlib.Path(specificPathToData)

        strPath = str(pathForReader)
        if "*" in strPath:
            pathsForReader = map(pathlib.Path, glob.iglob(strPath))
            return pathsForReader

        if not pathForReader.exists():
            raise IOError("{} does not exist.".format(pathForReader))

        return pathForReader
