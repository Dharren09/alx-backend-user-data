#!/usr/bin/env python3
"""function that returns a log mesaage obfuscated"""

import logging
import re
from typing import List
import csv
import os
import mysql.connector

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """creates a regex epresssion to match the fields to obfuscate
    then returns log message obfuscated"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the secure Holberton database"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")

    """Create a connection to the database"""
    connection = mysql.connector.connect(
        user=db_user,
        password=db_pwd,
        host=db_host,
        database=db_name
    )

    return connection


def main():
    """implements a function with no arg and returns nothing
    it obtains a connection to db, retrieves all rows and displays
    each row under a filtered format"""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


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
        message = super(RedactingFormatter, self).format(record)
        record = filter_datum(self.fields, self.REDACTION,
                              message, self.SEPARATOR)
        return record


if __name__ == "__main__":
    main()
