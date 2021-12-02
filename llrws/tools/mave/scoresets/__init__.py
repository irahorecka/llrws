import json
import os

SCORESETS_JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json")


def read_json(json_filepath):
    with open(json_filepath) as f:
        json_ = json.load(f)
    return json_


def write_to_json(json_content, json_filepath):
    with open(json_filepath, "w") as file:
        json.dump(json_content, file)
