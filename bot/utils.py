# -*- coding:utf-8; -*-

import datetime
import logging
import re

from bot import constants, ui

logger = logging.getLogger('MyTimeTable')


def time_to_str(time: datetime.time):
    return time.strftime('%H:%M')


def str_to_time(string: str):
    time = string.split(':')
    return datetime.time(hour=int(time[0]), minute=int(time[1]))


def parse_time(str_time):
    pattern = r'(?P<hour>\d{1,2}):?\.?(?P<minute>\d{1,2}) ?- ?(?P<action>.+)'
    time = re.findall(pattern, str_time, re.IGNORECASE)
    return {time_to_str(datetime.time(hour=int(note[0]), minute=int(note[1]))): note[2] for note in time}


def convert_time_to_msk(time: datetime.time, tz=0):
    return time.replace(hour=time.hour - tz)


def convert_time_from_msk(time: datetime.time, tz=0):
    return time.replace(hour=time.hour + tz)


def check_timetable(database):
    current = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
    current_time = current.time().replace(minute=current.minute + 9)
    current_weekday = list(constants.days_of_week_long)[current.weekday()]
    forward_time = current_time.replace(minute=current_time.minute + 2) if current_time.minute < 50 else \
        current_time.replace(hour=current_time.hour + 1, minute=current_time.minute - 49)
    timetables_to_notify = {}
    for user in database.get_all():
        user_timedelta = user.get('settings', {}).get('timezone', 0)
        note_time = user.get('timetable', {}).get(current_weekday, {})
        if not note_time:
            pass
        for time in note_time:
            if current_time < convert_time_to_msk(str_to_time(time), user_timedelta) <= forward_time:
                if timetables_to_notify.get(user['id']):
                    timetables_to_notify[user['id']].append({time: note_time[time]})
                else:
                    timetables_to_notify[user['id']] = [{time: note_time[time]}]

    return timetables_to_notify


def notify():
    from bot import bot, database
    raw_notes = check_timetable(database)
    ready_notes = {}

    logger.info('Notifying')

    for raw_note in raw_notes:
        ready_notes[raw_note] = ui.text['scheduled'].format(notes='\n'.join([' - '.join(*a.items()) for a in raw_notes[raw_note]]))

    for user in ready_notes:
        bot.send_message(user, ready_notes[user], parse_mode='HTML')
