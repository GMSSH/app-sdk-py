# -*- encoding: utf-8 -*-
import inspect
from typing import Any, List

from simplejrpc.exceptions import TypeError


def make_signature(fields: List[Any]):
    """
    The function `make_signature` creates a signature object for a function based on a list of field
    names.

    :param fields: A list of any type of objects
    :type fields: List[Any]
    :return: an instance of the `inspect.Signature` class.
    """
    """ """
    params = []
    for name, required in fields:
        if required:
            params.append(inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY))
        else:
            params.append(
                inspect.Parameter(name, inspect.Parameter.KEYWORD_ONLY, default=None)
            )
    return inspect.Signature(params)


def str2int(value: str | int, name: str):
    """ """
    if isinstance(value, int):
        return value
    if not value.isdigit():
        raise TypeError(f"Field {name}, expected integer")

    return int(value)
