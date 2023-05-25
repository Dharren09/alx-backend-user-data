#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import re
from typing import List

pii_fields = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """returns the obfuscated log message"""
    for field in fields:
        message_obfuscated = re.sub(f'{field}=.+?{separator}',
                                    f'{field}={redaction}{separator}', message)
        return message_obfuscated
