#!/usr/bin/env python3
""" Model for filtered data """
import re
import logging
import mysql.connector
from typing import List
from os import getenv

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ Create and  returns a logging.Logger object """
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    user_stream_header = logging.StreamHandler()
    user_stream_header.setFormatter(RedactingFormatter)
    user_data.addFilter(user_stream_header)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ connector to MySQL database """
    db_name = getenv("PERSONAL_DATA_DB_NAME")
    db_host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pass = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    try:
        db_connector = mysql.connector.connection.MySQLConnection(
            user=db_username,
            password=db_pass,
            host=db_host,
            database=db_name
        )
        return db_connector
    except mysql.connector.Error:
        return None


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """eturns the log message obfuscated"""
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*',
                  rf'\1={redaction}', message)


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
        """filter values in incoming log records """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)
