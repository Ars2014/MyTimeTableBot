# -*- coding:utf-8; -*-

from telebot import types

from bot import constants

buttons = {
    'main': [['Всё расписание', constants.emoji['change_timetable']],
             [constants.emoji['delete'], constants.emoji['settings'], constants.emoji['rate']]],
    'days': [list(constants.days_of_week_long.keys()) + [constants.emoji['cancel']]],
    'user_input': [constants.emoji['cancel']],
    'cancel': [['Главное меню']],
    'settings': [['Изменить часовой пояс'], ['Главное меню']],
    'timezones': [constants.timezones[x:x + 6] for x in range(0, len(constants.timezones), 6)]
}

text = {
    'main': '<strong>Главное меню</strong>\n\n\n📝 - Изменить расписание\n🗑 - Удалить запись\n⚙ - Настройки\n⭐ - Оцените бота',
    'days': '<strong>Выберете день недели:</strong>',
    'change': '<strong>Изменение расписания для {day}.</strong>\n\n\n Пример:\n<code>11:45 - Test\n11.34-Test</code>',
    'cancel': 'Отменено.',
    'success': 'Операция успешно завершена.',
    'timetable': '<strong>{day}:</strong>\n\n\n{timetable}',
    'rate': 'Пожалуйста, оцените меня здесь <a href="https://telegram.me/storebot?start=mytimetable_bot">Store bot</a>.',
    'settings': '<strong>Настройки:</strong>',
    'change_timezone': 'Отправьте свой часовой пояс в формате <code>+/-1</code> от '
                       'Московского времени.\n\n\n<strong>Например:</strong>\nДля Екатернинбурга: <code>+2</code>',
    'scheduled': '<strong>Через 10 минут должны произойти следующие события:</strong>\n\n\n{notes}',
    'day_empty': 'На данный день у вас ничего не записано. Отмена.',
    'choose_delete': '<strong>Выберете какую запись удалить:</strong>\n\n\n{notes}'
}

days_keyboard_inline = types.InlineKeyboardMarkup(row_width=4)
days_keyboard_inline.add(*[types.InlineKeyboardButton(day, callback_data=day) for day in constants.days_of_week_long.keys()])


def generate_menu(name):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for r in buttons[name]:
        keyboard.row(*r)
    return keyboard
