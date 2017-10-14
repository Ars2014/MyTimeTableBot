# -*- coding:utf-8; -*-

import datetime
import re


def parse_time(str_time):
    pattern = r'(?P<hour>\d{1,2}):?.?(?P<minute>\d{1,2}) ?- ?(?P<action>\w+)'
    time = re.findall(pattern, str_time, re.IGNORECASE)
    return [(datetime.time(hour=int(note[0]), minute=int(note[1])).strftime('%H:%M'), note[2]) for note in time]
