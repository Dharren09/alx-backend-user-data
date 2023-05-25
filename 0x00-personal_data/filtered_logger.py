#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import logging
import re
from typing import List

pii_fields = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """creates a regex epresssion to match the fields to obfuscate
    then returns log message obfuscated"""
    pattern = re.compile(r'(' + '|'.join(fields) + r')=[^' +
                         separator + r']+' + separator)
    return re.sub(pattern, lambda match: match.group(1) + '=' +
                  redaction + separator, message)


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
