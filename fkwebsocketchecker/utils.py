# coding=utf-8
import json


def format_endpoint(endpoint):
    if 'ws://' not in endpoint:
        endpoint = 'ws://' + endpoint

    return endpoint


def load_json(file_path):
    with open(file_path) as data_file:
        data = json.loads(data_file.read())

    return data
