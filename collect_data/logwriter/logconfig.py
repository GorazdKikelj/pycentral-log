# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
    Logging setup was inspired by mCoding YouTube channel:
    https://www.youtube.com/@mCoding
    https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging
    
    
"""
from logging import (
    Logger,
    getLogger,
    basicConfig,
    Filter,
    INFO,
    LogRecord,
    getLevelName,
)
from pathlib import Path
import json
import logging.config
import logging.handlers
from typing import Type

from typing_extensions import override
from xml.dom import ValidationErr

from . import C_LOG_DIR, C_DEBUG_LEVEL, C_LOG_CONFIG


class NonErrorFilter(Filter):
    @override
    def filter(self, record: LogRecord) -> bool | LogRecord:
        return record.levelno <= INFO


def setup_logging():
    """
    Set the logger object for logging into file and terminal.

    Constants:
    C_DEBUG_LEVEL   set the initial debug level for Terminal output.
                    This can be overriden by specifying debug level
                    with --debug_level parameter

    C_DEBUG_LEVEL_FILE set default debug level for log file. If set
                    to None it defaults to C_DEBUG_LEVEL

    C_LOG_CONFIG    points to the JSON config file

    C_LOG_DIR       default log directory

    """
    config_file = Path(C_LOG_CONFIG)
    with open(config_file, "r") as f_in:
        config = json.load(f_in)

    try:
        ln_log: str = Path(C_LOG_DIR + config["handlers"]["file"]["filename"])
        config["handlers"]["file"]["filename"] = ln_log
    except KeyError:
        pass

    logging.config.dictConfig(config)


def _create_logger(log_directory: str) -> Logger:

    Path(log_directory).mkdir(parents=False, exist_ok=True)

    setup_logging()

    #    logger: Logger = getLogger(__name__)
    logger: Logger = getLogger()

    basicConfig(
        filemode="a",
        level=C_DEBUG_LEVEL,
    )

    return logger


log_writer = _create_logger(log_directory=C_LOG_DIR)


def check_debug_level(debug_level: str) -> None:
    dbg_level = debug_level.upper()
    if not dbg_level in [
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]:
        log_writer.error(
            f"Unknown debug level {dbg_level}. Using {C_DEBUG_LEVEL} instead."
        )
        dbg_level = C_DEBUG_LEVEL

    log_writer.setLevel(dbg_level)
    for handler in log_writer.handlers:
        handler.setLevel(dbg_level)
    log_writer.info(f"__Debug level: {dbg_level}")

    return None
