#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    filter_datum - Redactes sensitive information from log line
"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """Redactes sensitive information from log line"""
    for field in fields:
        message = re.sub("({}=)(.*?){}".format(field, separator),
                         "\1{}{}".format(redaction, separator), message)
    return message
