# -*- encoding: utf-8 -*-
from simplejrpc import exceptions
from simplejrpc._mapping import DefaultMapping
from simplejrpc.app import ServerApplication
from simplejrpc.client import Request
from simplejrpc.config import Settings
from simplejrpc.i18n import T as i18n
from simplejrpc.interfaces import BaseServer, BaseValidator, ClientTransport, RPCMiddleware

try:
    # For python 3.8 and later
    import importlib.metadata as importlib_metadata
except ImportError:
    # For everyone else
    import importlib_metadata
try:
    __version__ = importlib_metadata.version("simplejrpc")
except importlib_metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
