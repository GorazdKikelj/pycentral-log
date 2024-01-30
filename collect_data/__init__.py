# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
"""

__all__ = ["collect_data"]
__author__ = "Gorazd Kikelj"
__version__ = "0.1.0"
__license__ = "MIT"


from .config import (
    C_LOG_DIR,
    C_DATA_DIR,
    C_CSV_DELIMITER,
    C_CSV_SN_COLUMN,
    C_JSON_CENTRAL,
    C_JSON_COMMANDS,
    C_JSON_FILTER,
    C_DEBUG_LEVEL,
    C_EVENT_LIST,
    C_REQUIRED_KEYS,
    C_TIMESTAMPS,
)

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

from .collect_data import run_collection
