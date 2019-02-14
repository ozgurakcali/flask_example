import datetime

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def convert_datetime_to_timestamp(datetime_object):
    """
    :param datetime_object: Datetime object to be converted into timestamp
    :return: Unix timestamp for provided datetime object
    """
    return (datetime_object - datetime.datetime(1970, 1, 1)).total_seconds()
