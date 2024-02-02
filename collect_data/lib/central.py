# -*- coding: utf-8 -*-
"""
    Author: Gorazd Kikelj
    
    gorazd.kikelj@gmail.com
    
"""
from time import sleep
from pycentral.base import ArubaCentralBase
from icecream import ic


def get_central_data(central, apipath: str, apiparams: dict = {"offset": 0}) -> dict:
    """
    Retrive prepared data from Aruba Central Instance

    Return : dictionary

        Retrived data is returned as dictionary

    Parameters:

    apipath: str
        REST API URL for returnig data

    apiparams: dict
        Parameters required for data filtering


    """
    apiPath = apipath
    apiMethod = "GET"
    apiParams = apiparams
    base_resp = central.command(
        apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams
    )
    if base_resp["code"] >= 400:
        print(
            f"Retrying GET request for {apiPath} status code {base_resp['code']} {base_resp['msg']['detail']}"
        )
        sleep(2)
        base_resp = central.command(
            apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams
        )
        print(
            f"Retried GET request for {apiPath} status code {base_resp['code']} {base_resp['msg']['detail']}"
        )

    return base_resp.get("msg")


def post_central_data(central, apipath: str, apidata: dict = {}) -> dict:
    """
    Submit data collection request to Aruba Central Instance

    Return: dictionary

        Return call result as dictionary

    Parameters:

    apipath: str
        REST API URL path for called function

    apidata: dict
        JSON debug commands

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
                            }
                        ]
        }

    """
    apiPath = apipath
    apiMethod = "POST"
    apiData = apidata
    base_resp = central.command(apiMethod=apiMethod, apiPath=apiPath, apiData=apiData)
    if base_resp["code"] >= 400:
        print(f"Retrying POST request for {apiPath} status code {base_resp['code']}")
        sleep(2)
        base_resp = central.command(
            apiMethod=apiMethod, apiPath=apiPath, apiData=apiData
        )
        print(f"Retried POST request for {apiPath} status code {base_resp['code']}")

    return base_resp["msg"]


def connect_to_central(central_info: dict) -> None:
    """
    Establish connection with Aruba Central instance

    Return: None

    Parameters:

    central_info : dict
        {
            "base_url": "< Central Instance API gateway URL >",
            "customer_id": "< Aruba Central Customer ID >",
            "client_id": "< API Token Client ID >",
            "client_secret": "< API Token Client Secret >",
            "username": "< GreenLake Username >",
            "password": "< GreenLake Password >"
        }
    or
        {
            "base_url": "< Central Instance API gateway URL >,
            "token": {
                        "access_token": "< Aruba Central REST API Access Token >",
                        "refresh_token": "< Aruba Central REST API Refresh Token >",
                     }
        }
    """
    token_store = {"type": "local", "path": "token"}
    central = ArubaCentralBase(
        central_info=central_info,
        token_store=token_store,
        ssl_verify=True,
    )
    return central


def get_per_ap_settings(central, serial_no) -> dict:
    """
    Return status data for specific AP
    """
    apipath = f"/configuration/v1/ap_settings_cli/{serial_no}"
    ap_data = get_central_data(central=central, apipath=apipath)
    if isinstance(ap_data, dict):
        return ap_data.get("aps")
    return None
