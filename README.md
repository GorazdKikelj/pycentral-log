### Collect log and debug data from devices managed by Aruba Central

Hewlett Packard Enterprise Aruba Central is unified network management platform
for wired, wireless and SD-WAN networks.

With Aruba Central REST API module pycentral it is possible to automate data
collection from devices managed by Aruba Central. 

With collect_data.py you can:

1. Select devices based on events
2. Use CSV file to select devices

More details about [Aruba Central REST API](https://developer.arubanetworks.com/aruba-central/docs/central-about)
[pycentral](https://developer.arubanetworks.com/aruba-central/docs/python-using-api-sdk) information is available on Aruba Developer hub.


### Installation

Requirements:

icecream
pycentral
python_dateutil

Installation:

1. Install prerequisites. 
2. Clone github to destination folder ur download zip file and unpack it in destination folder.

Setup:

1. Create [Aruba Central JSON Token](https://www.arubanetworks.com/techdocs/central/2.5.7/content/nms/api/apigw-bootstrap.htm) and save it. Default filename is central.json

2. Create debug commans JSON file. Available command depend on device type. More detail can be found in Aruba Central Swagger Page. 
Here is the example file to collect 
'''
show tech-support
show ap debug crash-info


{
    "device_type": "IAP",
    "commands": [
        {
            "command_id": 115,
            "arguments": [
                {
                    "name": "",
                    "value": ""
                }
            ]
        },
        {
            "command_id": 34,
            "arguments": [
                {
                    "name": "",
                    "value": ""
                }
            ]
        }
    ]
}
'''

3. Create filter JSON file, if you will select APs by event type

'''
{
    "device_type": "ACCESS POINT",
    "sort": "-timestamp",
    "event_type": "AP Exception",
    "from_timestamp": "2024-01-10"
}

All filter fields:
{
    "group": "string",
    "swarm_id": "string",
    "label": "string",
    "from_timestamp": "string YYYY MM DD hh:mm:ss", # it will be converted to int timestamp
    "to_timestamp": "string YYYY MM DD hh:mm:ss", # it will be converted to int timestamp
    "offset": integer,
    "limit": integer,
    "macaddr": "string",
    "bssid": "string",
    "hostname": "string",
    "device_type": "string", ["ACCESS POINT", "SWITCH", "GATEWAY", "CLIENT"]
    "sort": "string", ["-timestamp", "+timestamp"]
    "site": "string",
    "serial": "string",
    "level": "string", ["normal", "positive", "negative",  ]
    "event_description": "string",
    "event_type": "string", ["AP Exception", "AP Offline", "AP Online", "Security", ...]
    "fields": "string", comma separated list [number, level]
    "calculate_total": "boolean"
}
''' 

4. Create a csv file if you will select APs from CSV.


### Package structure

'''
|   README.md
|   Contrubutions.md
|
|---collect_data
|   |   collect_data.py
|   |   requirements.txt
|   |   ...
|   |
|   |---lib
|   |     arguments.py
|   |     central.py
|   |     logconfig.py
|   |     utilities.py
|   |     ...
|   |    
|   |---templates
|   |     ap_commands.json
|   |     central-token.json
|   |     central.json
|   |     commands.json
|   |     filter.json
|   |
--------docs
        |   ...

'''


usage: collect_data.py [-h] [--csv_input CSV_INPUT] [--csv_sn_column CSV_SN_COLUMN] 
                       [--csv_delimiter CSV_DELIMITER] [--json_central JSON_CENTRAL] 
                       [--json_filter JSON_FILTER] [--json_commands JSON_COMMANDS] 
                       [--event_list EVENT_LIST] [--data_directory DATA_DIRECTORY] 
                       [--start_date START_DATE]
                       [--end_date END_DATE] [--debug_level DEBUG_LEVEL]

........ Log collection App for Aruba Central REST API .....

options:
  -h, --help            show this help message and exit
  --csv_input CSV_INPUT
                        CSV input file containing list of AP serial numbers to collect data from. (optional, default=input.csv)
  --csv_sn_column CSV_SN_COLUMN
                        Column # or name where device Serial number is stored. (optional, default=0)
  --csv_delimiter CSV_DELIMITER
                        Column delimiter (optional, default=',')
  --json_central JSON_CENTRAL
                        JSON file with Aruba Central Access Token (Optional, default=central.json)
  --json_filter JSON_FILTER
                        JSON file with device select filter (optional, default=filter.json)
  --json_commands JSON_COMMANDS
                        JSON file with list of commands to execute for each device (optional, default=commands.json)
  --event_list EVENT_LIST
                        Summary Output of all events (optional, default=event_list.txt)
  --data_directory DATA_DIRECTORY
                        Directory for result files (optional, default=data/)
  --start_date START_DATE
                        Event start date in format YYYY-MM-DD (optional, default=<from filter.json>)
  --end_date END_DATE   Event end date in format YYYY-MM-DD (optional, default=now)
  --debug_level DEBUG_LEVEL
                        Set debul level to [NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL]

