# -*- coding:utf-8; -*-

from telebot import types

from bot import constants

buttons = {
    'main': [['Всё расписание'], [constants.emoji['settings'], constants.emoji['rate'], constants.emoji['change_timetable']]],
    'days': [constants.days_of_week_long.keys()],
    'user_input': [constants.emoji['cancel']],
    'cancel': [['Главное меню']],
}

text = {
    'main': '<strong>Главное меню</strong>\n\n\n⚙ - Настройки\n⭐ - Оцените бота\n📝 - Изменить расписание',
    'days': '<strong>Выберете день недели:</strong>',
    'change': '<strong>Изменение расписания для {day}.</strong>\n\n\n Пример:\n<code>11:45 - Test\n11.34-Test</code>',
    'cancel': 'Отменено.',
    'success': 'Операция успешно завершена.',
    'timetable': '<strong>{day}:</strong>\n\n\n{timetable}'
}


days_keyboard_inline = types.InlineKeyboardMarkup()
days_keyboard_inline.add(*[types.InlineKeyboardButton(day, callback_data=day) for day in constants.days_of_week_long.keys()])


def generate_menu(name):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for r in buttons[name]:
        keyboard.row(*r)
    return keyboard
