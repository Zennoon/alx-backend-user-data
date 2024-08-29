#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    filter_datum - Redactes sensitive information from log line
"""
import logging
import os
import re
from typing import List

import mysql.connector

PII_FIELDS = ("phone", "email", "name", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Custom formatter of the logged message"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Redactes sensitive information from log line"""
    for fld in fields:
        message = re.sub("{}=.*?{}".format(fld, separator),
                         "{}={}{}".format(fld, redaction, separator), message)
    return message


def get_logger() -> logging.Logger:
    """Returns custom logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.MySQLConnection(
        user=user,
        password=passwd,
        host=host,
        database=db
    )
    conn.connect()
    return conn


def main() -> None:
    """Main function"""
    conn = get_db()
    logger = get_logger()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    columns = cursor.column_names
    for row in cursor:
        zipped = zip(columns, list(row))
        message = " ".join(
            ["{}={};".format(field, value) for field, value in zipped]
        )
        logger.info(message)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
