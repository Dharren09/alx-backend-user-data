#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import re
from typing import List

pii_fields = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """create a regex to match the fields to obfuscate"""
    regex = r'({0}=)[^{1}]+'.format('|'.join(fields), separator)

    """returns the obfuscated log message"""
    return re.sub(regex, r'\1{0}'.format(redaction), message)
