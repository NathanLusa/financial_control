import re
import calendar
from datetime import datetime

from .exceptions import ConverterError


def first_day_month(date):
    return date.replace(day=1)


def last_day_month(date):
    last_day = calendar.monthrange(date.year, date.month)[1]
    return date.replace(day=last_day)


def str_to_date(date: str):
    regex_str = '(19|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'
    regex = re.compile(regex_str)

    if not regex.match(date):
        raise ConverterError(400, 'The date not match yyyy-mm-dd.')

    return datetime.strptime(date, '%Y-%m-%d').date()
