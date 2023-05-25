#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import re


def filter_datum(fields, redaction, message, separator):
    """creates a regular expression using 2 args then matches any
    specified feilds followed by a separator then captures the feild
    to be replaced"""
    return re.sub(r'({0})=[^{1}]+'.format('|'.join(fields), separator),
                  r'\1={0}'.format(redaction), message)
