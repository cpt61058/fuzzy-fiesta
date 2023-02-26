from typing import List
import json


def read_config():
    with open("../cfg/mapping.json", "r") as mapping:
        data = mapping.read()
    json_data = json.loads(data)
    return json_data


def read_usernames(data) -> List[str]:
    return list(data["urls"].values())


def read_names(data) -> List[str]:
    return list(data["urls"].keys())


def read_stats_url(data) -> str:
    return data["stats_url"]


def read_spreadsheet_id(data) -> str:
    return data["spreadsheet_id"]
