import asyncio
from enum import IntEnum
from importlib import import_module
from importlib.util import find_spec
import inspect
import sys
import typing
from typing import Protocol
import warnings

from typing_extensions import Literal


class Order(IntEnum):
    """Order to choose"""

    TO_RIGHT = -1
    TO_LEFT = 0


@typing.overload
def choice_in_order(
    module_names: typing.List[str],
    order: Order = Order.TO_RIGHT,
    do_import: Literal[True] = ...,
    default: typing.Optional[str] = None,
) -> typing.Any:
    ...


@typing.overload
def choice_in_order(
    module_names: typing.List[str],
    order: Order = Order.TO_RIGHT,
    do_import: Literal[False] = ...,
    default: typing.Optional[str] = None,
) -> str:
    ...


def choice_in_order(
    module_names: typing.List[str],
    order: Order = Order.TO_RIGHT,
    do_import: bool = False,
    default: typing.Optional[str] = None,
) -> typing.Union[str, typing.Any]:
    """Finds out installed module from list based on order
    :param module_names: list of module names
    :param order: order from worst to best to be installed
    :param do_import: should module be imported
    :param default: default module name [deprecated]
    :return: module if do_import else module_name
    """
    default_name = default or module_names[0]
    installed = [module_name for module_name in module_names if find_spec(module_name) is not None]
    if not installed and default is None:
        raise ModuleNotFoundError("No proper module was installed. " "List: {}".format(", ".join(module_names)))

    ordered_module_name = installed[order.value] if installed else default_name
    return ordered_module_name if not do_import else import_module(ordered_module_name)


class JSONModule(Protocol):
    def loads(self, s: str) -> dict:
        ...

    def dumps(self, o: dict) -> str:
        ...

    def load(self, f: str) -> dict:
        ...

    def dump(self, o: dict, f: str) -> None:
        ...


json: JSONModule = choice_in_order(["ujson", "hyperjson", "orjson"], do_import=True, default="json")

warnings.simplefilter("always", DeprecationWarning)
showwarning_ = warnings.showwarning


def showwarning(message, category, filename, lineno, file=None, line=None):  # noqa: ARG001
    new_message = f"{category.__name__}: {message}"
    if logging_module == "loguru":
        logger.opt(depth=2).log("WARNING", new_message)  # type: ignore
        return
    logger.log(
        logging.WARNING,
        new_message,
        stacklevel=4,
    )


logging_module = choice_in_order(["loguru"], default="logging")
if logging_module == "loguru":
    import logging
    import os

    if not os.environ.get("LOGURU_AUTOINIT"):
        os.environ["LOGURU_AUTOINIT"] = "0"
        os.environ["LOGURU_INFO_COLOR"] = "<bold><green>"
    from loguru import logger  # type: ignore

    if not logger._core.handlers:  # type: ignore

        def log_filter(record):
            if record["function"] == "<module>":
                record["function"] = "\b"
            return True

        log_format = (
            "<level>{level: <8}</level> <bold><level>|</level></bold> "
            "{time:YYYY-MM-DD HH:mm:ss.SSS} <bold><level>|</level></bold> "
            "{name}:{function}:{line}<bold><level> > </level></bold><level>{message}</level>"
        )

        # log_format = (
        #     "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        #     "<level>{level: <8}</level> | "
        #     "<blue>{process.name}({process.id})</blue>:<blue>{thread.name: <10}({thread.id: <5})</blue> | "
        #     "<cyan>{name}</cyan>:<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        # )

        logger.add(sys.stderr, format=log_format, enqueue=True, colorize=True, filter=log_filter)
        warnings.showwarning = showwarning

        class InterceptHandler(logging.Handler):
            def emit(self, record):
                try:
                    level = logger.level(record.levelname).name  # type: ignore
                except ValueError:
                    level = record.levelno
                frame, depth = sys._getframe(6), 6
                while frame and frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back  # type: ignore
                    depth += 1

                logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())  # type: ignore

        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


elif logging_module == "logging":
    """
    This is workaround for lazy formating with {} in logging.

    About:
    https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
    """
    import logging

    import colorama

    colorama.just_fix_windows_console()
    LEVEL_COLORS = {
        "DEBUG": colorama.Style.BRIGHT + colorama.Fore.BLUE,
        "INFO": colorama.Style.BRIGHT + colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Style.BRIGHT + colorama.Fore.RED,
    }

    loguru_like_format = (
        "<level>{levelname: <8}</level> <bold><level>|</level></bold> "
        "{asctime} <bold><level>|</level></bold> "
        "{module}:{funcName}:{lineno}<bold><level> > </level></bold><level>{message}</level>"
    )

    class ColorFormatter(logging.Formatter):
        def format(self, record):
            color = LEVEL_COLORS.get(record.levelname, "")
            log_format = (
                loguru_like_format.replace("<level>", color)
                .replace("</level>", colorama.Style.RESET_ALL)
                .replace("<bold>", colorama.Style.BRIGHT)
                .replace("</bold>", colorama.Style.RESET_ALL)
            )
            if not record.funcName or record.funcName == "<module>":
                record.funcName = "\b"
            frame = next(
                (
                    frame
                    for frame in inspect.stack()
                    if frame.filename == record.pathname and frame.lineno == record.lineno
                ),
                None,
            )
            if frame:
                module = inspect.getmodule(frame.frame)
                record.module = module.__name__ if module else "<module>"
            return logging.Formatter(
                log_format,
                datefmt=self.datefmt,
                style="{",
            ).format(record)

    logging.basicConfig(level=logging.DEBUG)
    logging.root.handlers[0].setFormatter(ColorFormatter())

    class LogMessage:
        def __init__(self, fmt, args, kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args)

    class StyleAdapter(logging.LoggerAdapter):
        def __init__(self, logger, extra=None):
            super().__init__(logger, extra or {})

        def log(self, level, msg, *args, **kwargs):
            if self.isEnabledFor(level):
                if "stacklevel" not in kwargs:
                    kwargs["stacklevel"] = 2
                msg, args, kwargs = self.process(msg, args, kwargs)
                self.logger._log(level, msg, args, **kwargs)

        def process(self, msg, args, kwargs):
            log_kwargs = {
                key: kwargs[key] for key in inspect.getfullargspec(self.logger._log).args[1:] if key in kwargs
            }
            if isinstance(msg, str):
                msg = LogMessage(msg, args, kwargs)
                args = ()
            return msg, args, log_kwargs

    warnings.showwarning = showwarning

    logger = StyleAdapter(logging.getLogger("FJP"))  # type: ignore
    logger.info("logging is used as the default logger, but we recommend using loguru instead")

if hasattr(asyncio, "WindowsProactorEventLoopPolicy") and isinstance(
    asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy  # type: ignore
):
    """
    This is a workaround for a bug in ProactorEventLoop:
    https://github.com/aio-libs/aiohttp/issues/4324

    This also can be fixed by using loop.run_until_complete instead of asyncio.run
    but I like to use asyncio.run because it's more readable, and not require to create new event loop.
    """
    from asyncio.proactor_events import _ProactorBasePipeTransport, _ProactorBaseWritePipeTransport
    from functools import wraps

    def silence_exception(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (AttributeError, RuntimeError) as e:
                if str(e) not in (
                    "'NoneType' object has no attribute 'send'",
                    "Event loop is closed",
                ):
                    raise

        return wrapper

    _ProactorBasePipeTransport.__del__ = silence_exception(_ProactorBasePipeTransport.__del__)  # type: ignore
    _ProactorBaseWritePipeTransport._loop_writing = silence_exception(  # type: ignore
        _ProactorBaseWritePipeTransport._loop_writing  # type: ignore
    )
