# -*- coding:utf-8; -*-

import logging
import sys

import telebot

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
    timetable = '\n'.join([' - '.join((a, b)) for a, b in timetables]) if timetables else 'Пусто.'
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


@bot.message_handler(func=lambda msg: msg.text in constants.days_of_week_long.keys() and states[msg.chat.id] == 'change')
def change_timetable_2(msg):
    keyboard = ui.generate_menu('user_input')
    msg_to_answer = bot.send_message(msg.chat.id, ui.text['change'].format(day=constants.days_of_week_long[msg.text]), reply_markup=keyboard,
                                     parse_mode='HTML')
    states[msg.chat.id] = msg.text
    bot.register_next_step_handler(msg_to_answer, change_timetable_3)


def change_timetable_3(msg):
    times = utils.parse_time(msg.text)
    timetables = {states[msg.chat.id]: times}
    database.add_timetable(msg.chat.id, timetables)
    keyboard = ui.generate_menu('cancel')
    bot.send_message(msg.chat.id, ui.text['success'], reply_markup=keyboard)

# TODO: settings and favorite
