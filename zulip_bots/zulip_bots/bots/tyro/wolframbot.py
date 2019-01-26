import sys
import os
sys.path.insert(0, os.getcwd())

import requests
from requests.exceptions import HTTPError, ConnectionError
from typing import Dict, Any
import json

WALFRAM_API_URL = "http://api.wolframalpha.com/v1/result"
API_KEY = "73KWR2-WKYXVRETG6"


def get_short_answer(query):
    query = query.strip()
    print(query)
    pars = {'appid': API_KEY, 'i': query}
    data = requests.get(WALFRAM_API_URL, pars)
    print(data.text)
    return data.text
