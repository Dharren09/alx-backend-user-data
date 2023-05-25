#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import logging
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """creates a regex epresssion to match the fields to obfuscate
    then returns log message obfuscated"""
    pattern = re.compile(r'(' + '|'.join(fields) + r')=[^' +
                         separator + r']+' + separator)
    return re.sub(pattern, lambda match: match.group(1) + '=' +
                  redaction + separator, message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object with the specified configuration."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    """Read the CSV file and extract field names"""
    with open("user_data.csv", "r") as file:
        reader = csv.reader(file)
        field_names = next(reader)

    """Create a StreamHandler with the RedactingFormatter"""
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=field_names)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values from the incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
