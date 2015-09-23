from .metadata import fullMetadata, metadata
from . import paths
# from info import __doc__

import inspect as __inspect
from . import accessors

__accessorsDict__ = { name.lower(): cls() for name, cls in __inspect.getmembers(accessors, __inspect.isclass) if not name.startswith('_') }

globals().update( __accessorsDict__ )

__all__ = list(__accessorsDict__.keys()) + ["fullMetadata", "metadata", "paths", "accessors"]