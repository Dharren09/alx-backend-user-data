#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import re
from typing import List

pii_fields = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """creates a regular expression using 2 args then matches any
    specified feilds followed by a separator then captures the feild
    to be replaced"""
    return re.sub(r'({0})=[^{1}]+'.format('|'.join(fields), separator),
                  r'\1={0}'.format(redaction), message)
