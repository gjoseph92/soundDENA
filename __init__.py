from .metadata import fullMetadata, metadata
from . import paths
# from info import __doc__

from . import accessor
from .accessors import accessorExports

accessors = { name: accessor.Accessor(parserFunc, pathToData) for name, (parserFunc, pathToData) in accessorExports.items() }

globals().update( accessors )

__all__ = list(accessors.keys()) + ["fullMetadata", "metadata", "paths"]

# clean up exported namespace
del accessors
del accessorExports
del accessor
