"""This project was generated with fastapi-mvc."""
import logging

from my_fastapi_project.wsgi import ApplicationLoader
from my_fastapi_project.version import __version__

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

__all__ = ("ApplicationLoader", "__version__")
