#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    filter_datum - Redactes sensitive information from log line
"""
import logging
import re
from typing import List, Sequence

PII_FIELDS = ("ip", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Custom formatter of the logged message"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(fields: Sequence[str], redaction: str,
                 message: str, separator: str) -> str:
    """Redactes sensitive information from log line"""
    for fld in fields:
        message = re.sub("{}=.*?{}".format(fld, separator),
                         "{}={}{}".format(fld, redaction, separator), message)
    return message


def get_logger() -> logging.Logger:
    """Returns custom logger"""
    logger = logging.getLogger("user_data")
    logger.propagate - False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger
