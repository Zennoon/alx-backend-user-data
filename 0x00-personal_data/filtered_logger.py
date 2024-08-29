#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    filter_datum - Redactes sensitive information from log line
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Redactes sensitive information from log line"""
    for field in fields:
        message = re.sub(field+"=.*?{}".format(separator),
                         field+"={}{}".format(redaction, separator), message)
    return message
