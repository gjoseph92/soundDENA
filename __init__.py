from .metadata import fullMetadata, metadata
from . import paths
# from info import __doc__

from .accessor import Accessor
from .accessors import accessorExports

accessors = { name: Accessor(parserFunc, pathToData) for name, (parserFunc, pathToData) in accessorExports.items() }

globals().update( accessors )

__all__ = list(accessors.keys()) + ["fullMetadata", "metadata", "paths", "Accessor"]

# clean up exported namespace
del accessors
del accessorExports
