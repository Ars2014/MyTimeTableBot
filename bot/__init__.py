# -*- coding:utf-8; -*-

import logging
import sys

import telebot
from apscheduler.schedulers.background import BackgroundScheduler

from bot import config, dbhandler, ui, constants, utils

logger = logging.getLogger('MyTimeTable')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_output_handler = logging.StreamHandler(sys.stdout)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)

logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config.token)
database = dbhandler.Database(host=config.db_host,
                              port=config.db_port,
                              user=config.db_user,
                              password=config.db_password)

states = {}

scheduler = BackgroundScheduler()


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda msg: msg.text == 'Главное меню')
def start(msg):
    keyboard = ui.generate_menu('main')
    bot.send_message(msg.chat.id, ui.text['main'], reply_markup=keyboard, parse_mode='HTML')
    states[msg.chat.id] = 'main'
    database.add_user(msg.chat.id)


@bot.message_handler(commands=['cancel'])
@bot.message_handler(func=lambda msg: msg.text == constants.emoji['cancel'])
def cancel(msg):
    states[msg.chat.id] = 'cancel'
    keyboard = ui.generate_menu('cancel')
    bot.send_message(msg.chat.id, ui.text['cancel'], reply_markup=keyboard)


@bot.message_handler(commands=['timetable'])
@bot.message_handler(func=lambda msg: msg.text == 'Всё расписание')
def get_timetable(msg):
    bot.send_message(msg.chat.id, ui.text['days'], reply_markup=ui.days_keyboard_inline, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data in constants.days_of_week_long.keys())
def timetable_for_day(call):
    timetables = database.get_timetable(call.from_user.id).get(call.data)
    timetable = '\n'.join([' - '.join((a, b)) for a, b in timetables.items()]) if timetables else 'Пусто.'
    txt = ui.text['timetable'].format(day=constants.days_of_week_long[call.data], timetable=timetable)
    try:
        bot.edit_message_text(txt, call.from_user.id, call.message.message_id, reply_markup=ui.days_keyboard_inline, parse_mode='HTML')
    except telebot.apihelper.ApiException:
        bot.answer_callback_query(call.id)


@bot.message_handler(commands=['change'])
@bot.message_handler(func=lambda msg: msg.text == constants.emoji['change_timetable'])
def change_timetable(msg):
    keyboard = ui.generate_menu('days')
    bot.send_message(msg.chat.id, ui.text['days'], reply_markup=keyboard, parse_mode='HTML')
    states[msg.chat.id] = 'change'


@bot.message_handler(func=lambda msg: msg.text in constants.days_of_week_long.keys() and states.get(msg.chat.id) == 'change')
def change_timetable_2(msg):
    if states[msg.chat.id] == 'cancel':
        return
    keyboard = ui.generate_menu('user_input')
    msg_to_answer = bot.send_message(msg.chat.id, ui.text['change'].format(day=constants.days_of_week_long[msg.text]), reply_markup=keyboard,
                                     parse_mode='HTML')
    states[msg.chat.id] = msg.text
    bot.register_next_step_handler(msg_to_answer, change_timetable_3)


def change_timetable_3(msg):
    if states[msg.chat.id] == 'cancel':
        return
    times = utils.parse_time(msg.text)
    timetables = {states[msg.chat.id]: times}
    database.add_timetable(msg.chat.id, timetables)
    keyboard = ui.generate_menu('cancel')
    bot.send_message(msg.chat.id, ui.text['success'], reply_markup=keyboard)


@bot.message_handler(commands=['rate'])
@bot.message_handler(func=lambda msg: msg.text == constants.emoji['rate'])
def rate(msg):
    bot.send_message(msg.chat.id, ui.text['rate'], parse_mode='HTML')


@bot.message_handler(commands=['settings'])
@bot.message_handler(func=lambda msg: msg.text == constants.emoji['settings'])
def settings(msg):
    keyboard = ui.generate_menu('settings')
    states[msg.chat.id] = 'settings'
    bot.send_message(msg.chat.id, ui.text['settings'], reply_markup=keyboard, parse_mode='HTML')


@bot.message_handler(commands=['change_timezone'])
@bot.message_handler(func=lambda msg: msg.text == 'Изменить часовой пояс')
def change_timezone(msg):
    keyboard = ui.generate_menu('timezones')
    msg_to_answer = bot.send_message(msg.chat.id, ui.text['change_timezone'], reply_markup=keyboard, parse_mode='HTML')
    bot.register_next_step_handler(msg_to_answer, change_timezone_2)


def change_timezone_2(msg):
    if states[msg.chat.id] == 'cancel':
        return
    timezone = msg.text
    keyboard = ui.generate_menu('cancel')
    database.change_settings(msg.chat.id, {'timezone': int(timezone)})
    bot.send_message(msg.chat.id, ui.text['success'], reply_markup=keyboard)


@bot.message_handler(commands=['del'])
@bot.message_handler(func=lambda msg: msg.text == constants.emoji['delete'])
def delete_timetable(msg):
    keyboard = ui.generate_menu('days')
    bot.send_message(msg.chat.id, ui.text['days'], reply_markup=keyboard, parse_mode='HTML')
    states[msg.chat.id] = 'delete'


@bot.message_handler(func=lambda msg: msg.text in constants.days_of_week_long.keys() and states.get(msg.chat.id) == 'delete')
def delete_timetable_2(msg):
    if states[msg.chat.id] == 'cancel':
        return
    timetable = database.get_timetable(msg.chat.id).get(msg.text)
    if not timetable:
        keyboard = ui.generate_menu('cancel')
        bot.send_message(msg.chat.id, ui.text['day_empty'], reply_markup=keyboard)
        return
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*[telebot.types.InlineKeyboardButton(time, callback_data=time) for time in timetable])
    notes = '\n'.join([' - '.join([a, b]) for a, b in timetable.items()])
    states[msg.chat.id] = msg.text
    bot.send_message(msg.chat.id, ui.text['choose_delete'].format(notes=notes), reply_markup=keyboard, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: states.get(call.from_user.id) in constants.days_of_week_long.keys())
def delete_timetable_3(call):
    database.delete_note(call.from_user.id, states[call.from_user.id], call.data)
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    keyboard = ui.generate_menu('cancel')
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, ui.text['success'], reply_markup=keyboard)


utils.notify()
scheduler.add_job(utils.notify, 'interval', seconds=600)
scheduler.start()
