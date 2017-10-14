# -*- coding:utf-8; -*-

import atexit
import logging

import rethinkdb as r

logger = logging.getLogger('MyTimeTable')


class Database:
    def __init__(self, host='localhost', port=28015, user='mytimetable', password='mytimetable_secret'):
        logger.info('Creating connection with DB')
        self.connection = r.connect(host, port, user=user, password=password)
        self.initialize_db()
        self.connection.use('mytimetable')
        atexit.register(self.close)

    def close(self):
        self.connection.close()
        logger.info('Connection to DB was closed')

    def initialize_db(self):
        try:
            r.db_create('mytimetable').run(self.connection)
            r.db('mytimetable').table_create('users').run(self.connection)
            logger.info('DB was successfully configured')
        except r.errors.ReqlOpFailedError:
            logger.info('DB was configured already')

    def add_user(self, uid):
        r.table('users').insert({'id': uid}).run(self.connection)

    def add_timetable(self, uid, timetable):
        r.table('users').get(uid).update({'timetable': timetable}).run(self.connection)

    def get_timetable(self, uid):
        return r.table('users').get(uid)['timetable'].run(self.connection)
