#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    filter_datum
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """
    Returns the given message/log line with the given fields redacted
    using the provided redaction string

    Args:
        fields (list): A list of the fields whose values need to be redacted
        from the message
        redaction (str): The string to be used to redact the field values
        message (str): The log line
        separator (str): The string separating the fields in the log line

    Returns:
        (str): The obfuscated/redacted message/log line
    """
    for field in fields:
        message = re.sub(r"({}=)(.*?){}".format(field, separator),
                         r"\1{}{}".format(redaction, separator), message)
    return message
