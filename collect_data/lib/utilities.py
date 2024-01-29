import os
import json
import sys
import csv
from pathlib import Path
from datetime import datetime
from dateutil import parser

from icecream import ic

C_TIMESTAMPS = ["from_timestamp", "to_timestamp"]


def parse_str(str, dict, sep=","):
    toks = str.split(sep)
    ret = 0
    for tok in toks:
        tok = tok.strip()
        tok = tok.lower()
        if tok in dict:
            ret = ret | dict[tok]
    return ret


def date_hook(obj) -> dict:
    """
    Convert JSON timestamps from string format to integer timestamp.
    Current timestamp fields are ["from_timestamp", "to_timestamp"]

    Parameters:

    obj - JSON object

    Return:

    Modified JSON object as dictionary

    """
    outDict = {}
    for key, value in obj.items():
        if key in C_TIMESTAMPS:
            outDict[key] = int(datetime.timestamp(parser.parse(value)))
        else:
            outDict[key] = value

    return outDict


def read_jsonfile(filename: str, object_hook=False) -> dict:
    """
    Extract  info from input JSON File

    During JSON load converts JSON string date fields to timestamps
    with date_hook procedure

    Parameters:

    filename - JSON file

    Return:

    JSON values in dictionary

    """
    jsondict = {}
    jsonfile = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), filename)
    if os.path.isfile(jsonfile):
        with open(jsonfile, "r") as infile:
            try:
                if object_hook:
                    jsondict = json.load(infile, object_hook=date_hook)
                else:
                    jsondict = json.load(infile)
            except Exception as err:
                logger.error("Error in Input JSON file: %s" % str(err))
                sys.exit("Error in Input JSON file: %s" % str(err))

        return jsondict
    else:
        logger.error("JSON input file %s not found. exiting..." % str(jsonfile))
        sys.exit("Error: json input file %s not found. exiting..." % str(jsonfile))


def get_ap_list_from_csv(filename: str, row_index: any, delimiter: str) -> dict:
    """
    Return dictionary of device serialnumbers from csv input file.

    Return:

        Dictionary. Key is Serial Number of device.

        {
            "<serial number>": "<job number|None>"
        }

    Parameters:

        filename: str
            filename of JSON file

        row_index: any
            numeric value represent the column in csv file, starting with 0.
            First line is data.

            non numeric value is the name of the column.
            First line is header.
    """
    aps = {}
    with open(filename, "r") as csv_file:
        ap_list = csv.reader(csv_file, delimiter=delimiter)
        if isinstance(row_index, int):
            col = row_index
        else:
            for row in ap_list:
                col = row.index(row_index)
                break
        for row in ap_list:
            aps[row[col]] = ""

    return aps


def get_debug_commands_from_json(filename: str) -> dict:
    """
    Return debug commands to be run from input file.

    Return:

        Dictionary
    """
    return read_jsonfile(filename=filename)


def get_filter_from_json(filename: str) -> dict:
    """
    Return filter dictionary for selecting devices from Aruba Central.

    Return:

        Dictionary

    """
    return read_jsonfile(filename=filename, object_hook=True)


def get_central_from_json(filename: str) -> dict:
    """
    Get Aruba Central token data from JSON file.

    Return:

        Dictionary. Aruba Central Token.
    """
    return read_jsonfile(filename=filename)


def check_path(path: str) -> None:
    """
    Check if directory exists and create it if not.

    Return: None

    Parameters:

        path:
            Directory path
    """
    print(f"__Create directory {path}")
    Path(path).mkdir(parents=False, exist_ok=True)

    return None


def create_filename(directory: str, filename: str) -> str:
    """
    Compose the full file path.

    Return: File path

    Parameters:
        directory: str
            Directory path

        filename: str
            Filename

    """
    event_file = os.path.join(os.path.dirname(directory), filename)
    return event_file
