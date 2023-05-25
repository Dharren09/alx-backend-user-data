#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import re


def filter_datum(fields, redaction, message, separator):
    """constructs a regular expression pattern which matches any feilds
    followed by any of the args"""
    regex = r'({0}=)([^{1}]+)'.format('|'.join(fields), separator)
    return re.sub(regex, r'\1{0}'.format(redaction), message)
