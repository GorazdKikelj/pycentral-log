# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
"""
#
# Default values
#
# Default debug level
#
C_DEBUG_LEVEL = (
    "INFO"  #''' Common debug level [NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL] '''
)
#
# Default directories
#
C_LOG_DIR = "log/"  #''' Log directory '''
C_DATA_DIR = "data/"  #''' Data directory '''
#
# Default CSV parameters
#
C_CSV_FILENAME = "input.csv"  #''' CSV input filename '''
C_CSV_DELIMITER = ","  #''' CSV field delimiter '''
C_CSV_SN_COLUMN = 0  #''' Serial Numebr Column. Column numbering is started by 0. '''
#
# Default filenames
#
C_JSON_CENTRAL = "central.json"  # Aruba Central REST API Authorization parameters
C_JSON_COMMANDS = "commands.json"  # Debug commands
C_JSON_FILTER = "filter.json"  # Event filer
C_EVENT_LIST = "event_list.txt"  # List of selected events
#
# For future use. List of fields in central.json
#
C_TOPIC_CUSTOMER = [
    "token",
    "access_token",
    "refresh_token",
    "base_url",
    "customer_id",
    "client_id",
    "client_secret",
    "username",
    "password",
]
C_TOPIC_COMMANDS = ["device_type", "commands", "command_id", "arguments"]
#
# For future use. List of required keys in parameter dictionary
#
C_REQUIRED_KEYS = ["central_info", "debug_command", "event_file"]
#
# List of date field to transform from date format to timestamp in filter.json
#
C_TIMESTAMPS = ["from_timestamp", "to_timestamp"]
#
C_GET_RETRY_COUNT = 20
