# -*- coding:utf-8; -*-

import logging

import cherrypy
import telebot

from bot import config, bot

logger = logging.getLogger('MyTimeTable')


class Server:
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return ''


if config.use_webhook:
    logger.info('Using webhook to get updates')

    bot.remove_webhook()
    bot.set_webhook(config.webhook_url_base + config.webhook_url_path)

    wsgiapp = cherrypy.Application(Server(), '/', {'/': {}})
else:
    logger.info('Using polling to get updates')
    bot.remove_webhook()
    bot.polling()
