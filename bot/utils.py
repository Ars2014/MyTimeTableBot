# -*- coding:utf-8; -*-

import datetime
import logging
import re

from daytime import Daytime

from bot import constants, ui

logger = logging.getLogger('MyTimeTable')


MSK_TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))


def parse_time(str_time):
    pattern = r'(?P<hour>\d{1,2}) ?[:|\.] ?(?P<minute>\d{1,2}) ?- ?(?P<action>.+)'
    notes = re.findall(pattern, str_time, re.IGNORECASE)
    return {'{0}:{1}'.format(note[0], note[1]): note[2] for note in notes}


def check_timetable(database):
    current_msk = Daytime.fromtime(datetime.datetime.now(MSK_TIMEZONE))
    current_weekday = constants.weekdays[datetime.datetime.now(MSK_TIMEZONE).weekday()]
    interval_start = current_msk + 540
    interval_stop = current_msk + 600
    print(interval_start, interval_stop)
    for_notifying = {}
    for user in database.get_all():
        user_delta = user.get('settings', {}).get('timezone', 0)
        timetable = user.get('timetable', {}).get(current_weekday, {})
        if timetable:
            for time, note in timetable.items():
                if interval_start < Daytime.strptime(time, '%H:%M') - datetime.timedelta(hours=user_delta) < interval_stop:
                    if for_notifying.get(user['id']):
                        for_notifying[user['id']].append({time: note})
                    else:
                        for_notifying[user['id']] = [{time: note}]

    return for_notifying


def notify(bot, database):
    raw_notes = check_timetable(database)
    print(raw_notes)
    ready_notes = {}

    logger.info('Notifying')

    for raw_note in raw_notes:
        ready_notes[raw_note] = ui.text['scheduled'].format(notes='\n'.join([' - '.join(*a.items()) for a in raw_notes[raw_note]]))

    for user in ready_notes:
        bot.send_message(user, ready_notes[user], parse_mode='HTML')
