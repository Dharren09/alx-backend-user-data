#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import re
from typing import List

pii_fields = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """creates a regex epresssion to match the fields to obfuscate"""
    pattern = re.compile(r'(' + '|'.join(fields) + r')=[^' +
                         separator + r']+' + separator)
    return re.sub(pattern, lambda match: match.group(1) + '=' +
                  redaction + separator, message)
