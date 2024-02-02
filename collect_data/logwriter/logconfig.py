# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
"""
from logging import Logger, getLogger, basicConfig
from pathlib import Path

from . import C_LOG_DIR, C_DEBUG_LEVEL


def _create_logger(log_directory: str) -> Logger:
    Path(C_LOG_DIR).mkdir(parents=False, exist_ok=True)

    logger: Logger = getLogger(__name__)

    basicConfig(
        filename=f"{log_directory}troubleshooting.log",
        filemode="a",
        format="%(asctime)s : %(levelname)s : %(module)s %(lineno)d : %(message)s",
        level=C_DEBUG_LEVEL,
    )

    return logger


logger = _create_logger(log_directory=C_LOG_DIR)


class Log_Writer:
    def __init__(self) -> None:
        self.msg = None

    def debug(self, msg) -> None:
        logger.debug(msg)
        print(msg)
        return None

    def info(self, msg) -> None:
        logger.info(msg)
        print(msg)
        return None

    def warning(self, msg) -> None:
        logger.warning(msg)
        print(msg)
        return None

    def error(self, msg) -> None:
        logger.error(msg)
        print(msg)
        return None

    def critical(self, msg) -> None:
        logger.critical(msg)
        print(msg)
        return None

    def setLevel(self, msg) -> None:
        logger.setLevel(msg)
        return None


log_writer = Log_Writer()
