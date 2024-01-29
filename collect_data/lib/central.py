import json
from pprint import pprint
from time import sleep
import csv
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
        print(f"Retrying POST request. Last status code {base_resp['code']}")
        sleep(2)
        base_resp = central.command(
            apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams
        )

    return base_resp["msg"]


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
        print(f"Retrying POST request. Last status code {base_resp['code']}")
        sleep(2)
        base_resp = central.command(
            apiMethod=apiMethod, apiPath=apiPath, apiData=apiData
        )

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
