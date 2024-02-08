#!/usr/bin/env python3
""" Model for filtered data """
import re
from typing import List
import logging


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

    def __init__(self, fields: List[str]) -> None:
        """ intilaize data """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
