import json
import re
from typing import Union


def read_json(filename: str, encoding: str = "utf-8") -> Union[list, dict]:
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]{1,63}@[a-zA-Z0-9.-]{1,180}\.[a-zA-Z]{2,10}$'
    return re.match(pattern, email) is not None
