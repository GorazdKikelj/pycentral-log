# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
"""
from datetime import datetime
from time import sleep
from icecream import ic

from .lib import get_per_ap_settings
from .logwriter import log_writer

try:
    from . import C_EVENT_LIST
except ImportError:
    C_EVENT_LIST = "event_list.txt"

try:
    from . import C_GET_RETRY_COUNT
except ImportError:
    C_GET_RETRY_COUNT = 40

try:
    from .lib import (
        get_central_data,
        post_central_data,
        connect_to_central,
        get_per_ap_settings,
        log_writer,
        create_filename,
        init_arguments,
        select_keys,
    )
except ImportError as err:
    print(f"Package error:\n{err}")
    exit()
"""

Instructions:


input.csv
    List of AP serial numbers to collect data from.
     

filter.json  
    Use subset of fields to filter events. Fields from_timestamp and to_timestamp will be converted
    to numeric timestamp. String representation in JSON file is for convenience.
    More information can be found in Aruba Central Swagger.

Example:
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

central.json
    Authorization data for REST API Gateway. 
    Use token or username/password. Do not use both. 
    
central_info = {
    "token": {
           "access_token": "string",
            "refresh_token": "string",
        },
    "base_url": "url string",
    "customer_id": "string",
    "client_id": "string",
    "client_secret": "string",
    "username": "string",
    "password": "string",
}

ap_debug.json
    List of debug commands sent to device.
    List of commands is available in Swagger.
    Use only commands appropriate for device type selected.

    From swagger:
        {
            "category": "System",
            "command": "show ap debug crash-info",
            "command_id": 34,
            "summary": "AP Crash Info"
        },
        {
            "category": "System",
            "command": "show tech-support",
            "command_id": 115,
            "summary": "AP Tech Support Dump"
        },
    
    Example command file:
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
"""

event_directory = ""


def get_ap_list_from_central(central, apiparams: dict = {"offset": 0}) -> dict:
    """
    Retreive all AP devices from central.

    """
    dev_list = get_central_data(
        central=central, apipath="/monitoring/v2/aps", apiparams=apiparams
    )

    return dev_list


def get_events_from_central(central, event_filter, event_file=C_EVENT_LIST):
    aps = {}
    event_list = get_central_data(
        central=central, apipath="/monitoring/v2/events", apiparams=event_filter
    )
    with open(event_file, "w") as event_file:
        for event in event_list.get("events"):
            aps[event.get("device_serial")] = None
            tm_stamp = datetime.fromtimestamp(float(event["timestamp"]) / 1000)
            event_file.write(
                f"{tm_stamp.isoformat()}, {event.get('device_type')}, {event.get('device_serial')}, {event.get('hostname')}, {event.get('event_type')}, {event.get('tool_tip_description')}"
            )

    return aps


def get_session_id_from_central(central, serial: str):
    """
    Get current running session id for the device
    """
    apiparams: dict = {"offset": 0}
    apipath: str = f"/troubleshooting/v1/devices/{serial}/session"
    msg = get_central_data(central=central, apipath=apipath, apiparams=apiparams)
    if isinstance(msg, dict):
        return msg.get("session_id")
    return None


def schedule_debug_command(central, serial_no, commands):
    response = post_central_data(
        central=central,
        apipath=f"/troubleshooting/v1/devices/{serial_no}",
        apidata=commands,
    )
    if response.get("status") in ["RUNNING"]:
        response["session_id"] = get_session_id_from_central(
            central=central, serial=serial_no
        )
    log_writer.info(
        f"{response.get('session_id')} : {response.get('status')} : {response.get('message')} : {response.get('hostname')}"
    )

    return response.get("session_id")


def get_debug_command_result(central, serial_no, session_id):
    if isinstance(session_id, bool):
        session_id = get_session_id_from_central(central=central, serial=serial_no)

        if not session_id:
            return {"status": None}
    count = 0
    response = {"status": None}

    while (response.get("status") != "COMPLETED") and (count < C_GET_RETRY_COUNT):
        response = get_central_data(
            central=central,
            apipath=f"/troubleshooting/v1/devices/{serial_no}",
            apiparams={"session_id": session_id},
        )
        if isinstance(response.get("status"), int):
            msg = get_per_ap_settings(central=central, serial_no=serial_no)
            log_writer(f"Get debug command result {msg}")
            if not msg:
                break
            if msg.get("status") == "Down":
                break

        log_writer.info(
            f"{session_id} : {response.get('status')} : {response.get('message')} : {response.get('hostname')}"
        )
        count += 1
        if response.get("status") == "COMPLETED":
            break
        sleep(5)

    return response


def save_debug_info(central, ap_list) -> dict:
    retry_session = {}
    for row in ap_list:
        result = get_debug_command_result(
            central=central, serial_no=row, session_id=ap_list[row]
        )
        fl = open(
            create_filename(directory=event_directory, filename=f"{row}.txt"),
            "w",
            encoding="utf-8",
            errors="ignore",
        )
        try:
            fl.write(result.get("output"))
        except TypeError:
            fl.write(f"Serial No: {row}, Session ID: {ap_list[row]}\n{result}\n")
            retry_session[row] = True
        fl.close()
    return retry_session


def retry_collect_debug_data(central, retry_session):
    log_writer.info(f"Total debug APs to retry: {len(retry_session)}")
    count = 0
    while (len(retry_session) > 0) and (count < 10):
        retry_session = save_debug_info(central=central, ap_list=retry_session)
        count += 1
        print(f"Retry loop {count}")

    return None


def collect_debug_data(central, serial_list, commands_json):
    job_list = {}
    for row in serial_list:
        job_id = schedule_debug_command(
            central=central, serial_no=row, commands=commands_json
        )
        if job_id:
            job_list[row] = job_id

    log_writer.info(
        f"Total debug AP requested: {len(serial_list)}, total AP submited: {len(job_list)}"
    )

    if len(job_list) > 0:
        retry_collect_debug_data(
            central=central,
            retry_session=save_debug_info(central=central, ap_list=job_list),
        )

    return None


def run_collection():
    params = init_arguments()
    central = connect_to_central(central_info=params.get("central_info"))

    serial_list = params.get("device_list")

    global event_directory
    event_directory = params["event_file"].get("directory")
    event_file = create_filename(
        directory=event_directory,
        filename=params["event_file"].get("filename"),
    )

    if not serial_list:
        serial_list = get_events_from_central(
            central=central,
            event_filter=params.get("event_filter"),
            event_file=event_file,
        )
    if params["condition"]["inverse_search"]:
        all_devices = get_ap_list_from_central(central=central)
        device_list = select_keys(
            all_keys=all_devices.get("aps"),
            filter_keys=serial_list,
            filter_field="serial",
        )
        log_writer.info(
            f"# all devices: {len(all_devices['aps'])} skipped devices: {len(serial_list)} selected devices: {len(device_list)}"
        )
        serial_list = device_list

    collect_debug_data(
        central=central,
        serial_list=serial_list,
        commands_json=params.get("debug_command"),
    )
    return None


def main():
    run_collection()


if __name__ == "__main__":
    main()
