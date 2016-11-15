from . import paths

import pandas as pd
import pathlib
import glob
import traceback
import sys

class Accessor:
    def __init__(self, parserFunc, pathToData):
        """
        Instantiate an Accessor for a specific filetype by giving a function
        to parse that kind of file, and where that file is located.

        Parameters
        ----------
        parserFunc : function
            A function which, given the path(s) to a file,
            parses and returns the data. This overrides the
            :meth:`parse` method of the instance.
        pathToData : str, pathlib.Path, or function
            Where to find the filetype in a site's :ref:`data directory <dataDir>`


        The docstring of ``parserFunc`` also will become the docstring of the Accessor instance.

        If **pathToData** is a string or pathlib.Path, it should be the path to this
        filetype *relative* to a :ref:`data directory <dataDir>`. The path can look like a
        Python format string that takes the keyword arguments ``unit``, ``site``, and ``year``.
        If the path contains a ``*`` character, it will also be passed to ``glob``,
        and the resulting list will be converted to pathlib.Paths and returned.
        (In this case, the ``parserFunc`` should also expect a list of paths.)

        Examples for ``pathToData``:

            * ``"01 DATA/PHOTOS/CardinalPhotoComposite_{unit}{site}.jpg"``
            * ``soundDENA.paths.spl / "SRCID_{unit}{site}.txt"``
            * ``soundDENA.paths.nvspl / "NVSPL_{unit}{site}*.txt"``

        If **pathToData** is a function, it should take the details of a specific site
        and return the path to the file(s) within that site, with this signature:

        .. function:: pathToData(dataDir, unit, site, year, **kwargs)

            :param pathlib.Path dataDir: The root data directory for a site
            :param str unit: Unit of the site
            :param str site: Site code of the site
            :param str year: Year of the site
            :param kwargs: Any keyword arguments related to path selection.
                           The same keyword arguments will be given to both **pathToData**
                           and **parserFunc**, so they should both be able to handle unexpected
                           keyword arguments by having **kwargs as the last item in their
                           argument lists.

            :return: Varies; the result is passed directly to ``parserFunc``.
                     Often, a pathlib.Path or list of pathlib.Path to the file(s)
                     to be parsed within the specific site's data directory.
        """
        self.parse = parserFunc
        if hasattr(pathToData, "__call__"):
            self._filepath = pathToData
        else:
            self.pathToData = pathToData
        self.__doc__ = self.parse.__doc__

    def __call__(self, sites, quiet= True, **kwargs):
        """
        Iterate site-by-site over a type of data.

        Data is yielded in the same order as the given sites,
        though some sites may be missing if they lack data.

        Parameters
        ----------
        sites : iterable
            :ref:`siteID` strings, or a pandas structure indexed by :ref:`siteID`
        quiet : boolean, optional
            Whether to not print info about any errors that occur
        kwargs
            Any keyword arguments specific to this filetype's :meth:`parse` or ``pathToData`` function

        Yields
        ------
        data : varies
            Data from each site in the format returned by :meth:`parse`
        unit : str
        site : str
        year : str
        """
        ## TODO: progress bar?
        for dataDir, unit, site, year in paths.dataDirs(sites, quiet= quiet):
            try:
                data = self.access((dataDir, unit, site, year), **kwargs)
                yield data, unit, site, year
            except KeyboardInterrupt:
                print("*** KeyboardInterrupt: halting execution ***")
                sys.exit(1)
            except OSError as e:
                if not quiet: print( e )
            except:
                # TODO: clearer error handling
                # print( _sys.exc_info()[0] )
                if not quiet: print( "Error when processing {}:".format(dataDir) )
                if not quiet: print( traceback.format_exc() )
                continue

    def all(self, sites, quiet= True, **kwargs):
        """
        Read data from all specified sites into a single DataFrame or dict.

        Parameters
        ----------
        sites : iterable
            :ref:`siteID` strings, or a pandas structure indexed by :ref:`siteID`
        quiet : boolean, optional
            Whether to not print info about any errors that occur
        kwargs
            Any keyword arguments specific to this filetype's :meth:`parse` or ``pathToData`` function

        Returns
        -------
        NDFrame or dict
            If :meth:`parse` retuns a pandas NDFrame for each site, all sites will be
            concatenated into one NDFrame, with :ref:`siteID` as outermost level of hierarchical index.
            Otherwise, returns a dict of ``{ siteID: data }``
        """

        results = { paths.siteID(unit, site, year): data for data, unit, site, year in self.__call__(sites, quiet= quiet, **kwargs) }
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

    def paths(self, sites, quiet= True, **kwargs):
        """
        Iterate site-by-site over the paths to this sort of data file.

        Parameters
        ----------
        sites : iterable of str, or NDFrame
            :ref:`siteID` strings, or a pandas structure indexed by :ref:`siteID`
        kwargs
            Any keyword arguments specific to this filetype's ``pathToData`` function

        Yields
        ------
        path : (list of) pathlib.Path
            Path(s) to the data file(s) for the site
        unit : str
        site : str
        year : str
        """
        for dataDir, unit, site, year in paths.dataDirs(sites, quiet= quiet):
            try:
                yield self._filepath(dataDir, unit, site, year, **kwargs), unit, site, year
            except OSError:
                continue

    def access(self, site, **kwargs):
        """
        Read data from one site.

        Parameters
        ----------
        site
            A single site or data directory specifier:

                * :ref:`siteID` string
                * pathlib.Path to a :ref:`data directory <dataDir>`
                * tuple of (unit, site, year) (all strings)
                * tuple of (dataDir, unit, site, year) (all strings, dataDir as pathlib.Path)
        kwargs
            Any keyword arguments specific to this filetype's :meth:`parse` or ``pathToData`` function

        Returns
        -------
        varies
            The result of the instance's :meth:`parse` function (typically a pandas DataFrame or Panel)
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

        filePath = self._filepath(dataDir, unit, site, year, **kwargs)
        return self.parse(filePath, **kwargs)

    @staticmethod
    def parse(filepath, **kwargs):
        """
        Parse data from disk located at filepath.
        This method is overridden in each instance by passing a parse function
        into :meth:`__init__`.

        All parse functions should have this signature:

        Parameters
        ----------
        filepath : pathlib.Path, or iterable of pathlib.Path
            The path(s) from which to read data
        kwargs
            Any keyword arguments specific to reading this filetype

        Returns
        -------
        varies
            Depends on what type of data is read. Typically, a pandas NDFrame.
        """
        raise NotImplementedError
    
    def _filepath(self, dataDir, unit, site, year, **kwargs):
        """
        Return the path (or list of paths) to the data file(s) for the given site of this type.
        This method can be overridden in an instance by passing a function as ``pathToData``
        in :meth:``__init__``.

        Otherwise, the default implementation fills in ``self.pathToData`` as a template.
        ``pathToData`` (passed in :meth:`__init__`) can be a pathlib.Path that looks like a
        Python format string, i.e. ``soundDENA.paths.spl / "SRCID_{unit}{site}.txt"``.
        It is formatted with keyword arguments for unit, site, and year,
        and joined onto the root data directory for the site.
        If the path contains a ``*`` character, it will be passed to ``glob``,
        and the resulting list will be converted to pathlib.Paths and returned.
        """
        specificPathToData = str(self.pathToData).format(unit= unit, site= site, year= year)
        pathForReader = dataDir / pathlib.Path(specificPathToData)

        strPath = str(pathForReader)
        if "*" in strPath:
            pathsForReader = map(pathlib.Path, glob.iglob(strPath))
            return pathsForReader

        if not pathForReader.exists():
            raise IOError("{} does not exist.".format(pathForReader))

        return pathForReader
