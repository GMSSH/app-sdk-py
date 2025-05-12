# -*- encoding: utf-8 -*-
import atexit
import inspect
import os
from functools import partial, wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from jsonrpcserver import method
from loguru import logger
from wtforms import Form, ValidationError

from simplejrpc import exceptions
from simplejrpc._sockets import JsonRpcServer
from simplejrpc.config import Settings
from simplejrpc.interfaces import RPCMiddleware
from simplejrpc.parse import *
from simplejrpc.response import raise_exception
from simplejrpc.schemas import BaseForm


class ServerApplication:
    """ """

    def __init__(
        self,
        socket_path: str,
        config: Optional[object] = Settings(),
        config_path: Optional[str] = None,
    ):
        self.server = JsonRpcServer(socket_path)
        self.config_path = config_path
        self.config = config
        if self.config_path is not None:
            self.from_config(config_path=self.config_path)

    def from_config(
        self,
        config_content: Optional[Dict[str, Any]] = None,
        config_path: Optional[str] = None,
    ):
        """ """
        if config_content:
            self.config = Settings(config_content)
        if config_path:
            """ """
            config_content = self.load_config(config_path)
        return self.config

    def route(self, name: Optional[str] = None, form: Optional[Form] = BaseForm, fn=None):
        """路由装饰器"""
        if fn is None:
            return partial(self.route, name, form)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            """ """
            if form:
                params = dict(zip(inspect.getfullargspec(fn).args, args))
                params.update(kwargs)
                form_validate = form(**params)
                if not form_validate.validate():
                    for _, errors in form_validate.errors.items():
                        for error in errors:
                            raise_exception(ValidationError, msg=error)

            return fn(*args, **kwargs)

        method(wrapper, name=name or fn.__name__)
        return wrapper

    def load_config(self, config_path: str):
        """ """

        if not os.path.exists(config_path):
            """ """
            raise exceptions.FileNotFoundError(f"Not found path {config_path}")

        path = Path(config_path)
        base_file = path.name
        _, filetype = base_file.split(".")

        match filetype:
            case "yml" | "yaml":
                parser = YamlConfigParser(config_path)
            case "ini":
                parser = IniConfigParser(config_path)
            case "json":
                parser = JsonConfigParser(config_path)
            case _:
                raise exceptions.ValueError("Unable to parse the configuration file")
        config_content: Dict[str, Any] = parser.read()
        self.config = Settings(config_content)
        return config_content

    def setup_logger(self, config_path: str):
        """ """
        config_content = self.load_config(config_path)

        # NOTE:: logger必须携带且sink必须携带
        if "sink" not in config_content.get_section("logger", {}):
            raise exceptions.AttributeError("Not found logger sink config")

        sink = config_content.logger.sink
        os.makedirs(Path(sink).parent, exist_ok=True)
        logger.add(**config_content.get_section("logger"))

    def clear_socket(self):
        """ """
        self.server.clear_socket()

    def middleware(self, middleware_instance: RPCMiddleware):
        """中间件配置"""
        return self.server.middleware(middleware_instance)

    async def run(self):
        """ """
        atexit.register(self.clear_socket)
        await self.server.run()
