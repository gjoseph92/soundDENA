from . import accessors
from . import paths

# because __init__.py imports * from this file, we don't want
# to add these modules to soundDB's namespace
import sys as _sys
import traceback as _traceback

"""
Mappers - apply an accessor to multiple sites.
          This logic handles finding data directories
          for all sites, handling missing data, and parallelizing accessors

Takes: an iterable of sites (typically a DataFrame indexed by site ID)
Yields: tuple of
        0 - pandas DataFrame for each site of whatever kind of data you asked for,
            as read by the appropriate Reader
        1 - unit
        2 - site
        3 - year
"""

def _mapper(accessorFunc):
    def mapperFunc(sites, pathsOnly= False, **kwargs):

        for dataDir, unit, site, year in paths.dataDirs(sites):
            try:
                data = accessorFunc(dataDir, pathsOnly= pathsOnly, **kwargs)
                yield data, unit, site, year
            except OSError as e:
                print( e )
            except:
                # TODO: clearer error handling
                # print( _sys.exc_info()[0] )
                print( "Error when processing {}:".format(dataDir) )
                print( _traceback.format_exc() )
                continue
    return mapperFunc

## A graceful, yet also hack-y way of wrapping every accessor method in a mapper,
## and making them accessible at the module level.
import inspect

_mappers = { name: _mapper(method) for name, method in inspect.getmembers(accessors, inspect.isroutine) if not name.startswith('_') }

# When this file is imported, globals() affects the module's namespace, not the whole global namespace.
# So all the mappers will be accessible by name within this module (as mapper.nvspl, for example).
globals().update( _mappers )