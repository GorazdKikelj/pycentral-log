# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
"""
import argparse
import sys
from datetime import datetime
from dateutil import parser


from collect_data import (
    C_DEBUG_LEVEL,
    C_EVENT_LIST,
    C_DATA_DIR,
    C_CSV_DELIMITER,
    C_CSV_SN_COLUMN,
    C_JSON_CENTRAL,
    C_JSON_COMMANDS,
    C_JSON_FILTER,
    C_REQUIRED_KEYS,
)

from . import (
    get_ap_list_from_csv,
    get_debug_commands_from_json,
    get_filter_from_json,
    get_central_from_json,
    check_path,
)

from collect_data.logwriter import log_writer, check_debug_level


def define_arguments():
    """
    This function defines a parser and help strings for script arguments.

    Returns:
        parser (ArgumentParser): A ArgumentParser varaible that contains all
                                 input parameters passed during script execution
    """
    parser = argparse.ArgumentParser(
        description="........ \
             Log collection App for Aruba Central REST API ....."
    )
    parser.add_argument(
        "--csv_input",
        required=False,
        help="CSV input file containing list of AP serial numbers \
                        to collect data from. (optional)",
    )
    parser.add_argument(
        "--csv_sn_column",
        required=False,
        help="Column # or name where device Serial number is stored. \
                        (optional, default=0)",
        default=C_CSV_SN_COLUMN,
    )
    parser.add_argument(
        "--csv_delimiter",
        required=False,
        help="Column delimiter (optional, default=',')",
        default=C_CSV_DELIMITER,
    )

    parser.add_argument(
        "--json_central",
        required=False,
        help="JSON file with Aruba Central Access Token (Optional, default=central.json)",
        default=C_JSON_CENTRAL,
    )
    parser.add_argument(
        "--json_filter",
        required=False,
        help="JSON file with device select filter (optional, default=filter.json)",
        default=C_JSON_FILTER,
    )
    parser.add_argument(
        "--json_commands",
        required=False,
        help="JSON file with list of commands to execute for each device \
                        (optional, default=commands.json)",
        default=C_JSON_COMMANDS,
    )
    parser.add_argument(
        "--event_list",
        required=False,
        help="Summary Output of all events (optional, default=event_list.txt)",
        default=C_EVENT_LIST,
    )
    parser.add_argument(
        "--data_directory",
        required=False,
        help=f"Directory for result files (optional, default={C_DATA_DIR})",
        default=C_DATA_DIR,
    )
    parser.add_argument(
        "--start_date",
        required=False,
        help="Event start date in format YYYY-MM-DD (optional, default=<from filter.json>)",
    )
    parser.add_argument(
        "--end_date",
        required=False,
        help="Event end date in format YYYY-MM-DD (optional, default=now)",
    )
    parser.add_argument(
        "--debug_level",
        required=False,
        help="Set debug level to [NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL]",
        default=None,
    )
    parser.add_argument(
        "--inverse_search",
        required=False,
        help="Inverse search condition. Return only devices not in input CSV or do not have event from filter.json present",
        default=False,
        action="store_true",
    )

    return parser


def process_arguments(args):
    """
    This function processes the input arguments supplied during script
    execution and stores them as param_dict variable.

    Returns:
        param_dict: A dictionary of key value pairs required for script exec.
    """
    param_dict = {}

    # Extract customer info from input JSON File

    debug_level = args.debug_level
    if debug_level:
        check_debug_level(debug_level)

    if args.csv_input:
        csv_file = args.csv_input
        csv_sn_column = args.csv_sn_column
        csv_delimiter = args.csv_delimiter
        if csv_delimiter in ["\\t", "tab", "Tab"]:
            csv_delimiter = "\t"
        param_dict["device_list"] = get_ap_list_from_csv(
            filename=csv_file, row_index=csv_sn_column, delimiter=csv_delimiter
        )
        log_writer.info(
            f"__Using device list from CSV file {csv_file}. Serial number column is {csv_sn_column}"
        )
    else:
        filter_file = args.json_filter
        param_dict["event_filter"] = get_filter_from_json(filename=filter_file)
        if args.start_date:
            param_dict["event_filter"]["from_timestamp"] = int(
                datetime.timestamp(parser.parse(args.start_date))
            )
        if args.end_date:
            param_dict["event_filter"]["to_timestamp"] = int(
                datetime.timestamp(parser.parse(args.end_date))
            )
        log_writer.info(
            f'__Using device list from Aruba Central event filter {param_dict["event_filter"]}'
        )

    central_file = args.json_central
    param_dict["central_info"] = get_central_from_json(filename=central_file)

    commands_file = args.json_commands
    param_dict["debug_command"] = get_debug_commands_from_json(filename=commands_file)
    log_writer.info(f'__Debug commands: {param_dict.get("debug_command")}')

    param_dict["event_file"] = {
        "filename": args.event_list,
        "directory": args.data_directory,
    }
    check_path(path=param_dict["event_file"]["directory"])
    log_writer.info(f'__Output Event file is {param_dict.get("event_file")}')

    param_dict["condition"] = {"inverse_search": args.inverse_search}
    log_writer.info(f"__Search conditions: {param_dict.get('condition')}")
    return param_dict


def validate_input_dict(inputDict, required_keys=C_REQUIRED_KEYS):
    """
    This function checks if all the required details provided in the input JSON file.
    """
    log_writer.info("Validating Input Dict...")

    # Check if required keys are present in the input
    input_key_error = []

    event_filter = inputDict.get("event_filter")
    if event_filter:
        start_date = (
            event_filter.get("from_timestamp")
            if event_filter.get("from_timestamp")
            else int(datetime.timestamp(datetime.now() - datetime.timedelta(hours=3)))
        )
        end_date = (
            event_filter.get("to_timestamp")
            if event_filter.get("to_timestamp")
            else int(datetime.timestamp(datetime.now()))
        )
        if start_date > end_date:
            input_key_error.append(f"Start time is higher than end time")

    error_str = ""
    if input_key_error:
        key_str = "{}".format(str(input_key_error))
        error_str = error_str + "\nError: " + key_str

    if error_str and error_str != "":
        log_writer.error(error_str)
        sys.exit(error_str)

    return None


def init_arguments() -> dict:
    """
    Initialize all parameters from input files.

    Return:
        Dictionary:

        param_dict: {'central_info': {'base_url': '',
                                  'client_id': '',
                                  'client_secret': '',
                                  'customer_id': '',
                                  'password': '',
                                  'username': ''},
                 'debug_command': {'commands': [{'arguments': [{'name': '', 'value': ''}],
                                                 'command_id': 115}],
                                   'device_type': 'IAP'},
                 'event_file': {'filename': 'event_list.txt',
                                'directory': 'data'},
                 'event_filter': {'device_type': 'ACCESS POINT',
                                  'event_type': 'AP Exception',
                                  'from_timestamp': 1701385200,
                                  'sort': '-timestamp',
                                  'to_timestamp': 1705273200}}

    """
    parser = define_arguments()
    args = parser.parse_args()
    param_dict = process_arguments(args)
    validate_input_dict(inputDict=param_dict)

    return param_dict
