# moodle_api.py

import os
from requests import post
from dotenv import load_dotenv

# Load token dan URL dari file .env
load_dotenv()

KEY = os.getenv("MOODLE_TOKEN")
URL = os.getenv("MOODLE_URL")
ENDPOINT = "/webservice/rest/server.php"

def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Convert nested dicts/lists into flat dictionary for Moodle API."""
    if out_dict is None:
        out_dict = {}

    if not isinstance(in_args, (list, dict)):
        out_dict[prefix] = in_args
        return out_dict

    if prefix == '':
        prefix = '{0}'
    else:
        prefix += '[{0}]'

    if isinstance(in_args, list):
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif isinstance(in_args, dict):
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    """Calls a Moodle WS function."""
    if not KEY or not URL:
        raise EnvironmentError("MOODLE_TOKEN or MOODLE_URL not set in .env")

    params = rest_api_parameters(kwargs)
    params.update({
        "wstoken": KEY,
        "moodlewsrestformat": "json",
        "wsfunction": fname
    })

    response = post(URL + ENDPOINT, params)
    try:
        data = response.json()
    except Exception:
        raise ValueError("Invalid JSON response from Moodle")

    if isinstance(data, dict) and data.get("exception"):
        raise RuntimeError(f"Moodle API Error: {data.get('message')}")

    return data
