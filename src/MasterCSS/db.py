"""
db.py module contains database setup.
Currently using MySQL, awaiting reply from teaching team if NoSQL is allowed.
"""
from flask import current_app, g
import pymysql


def init_db():
    # obtain database cursor
    cursor = g.db.cursor()
    # initialise database if not exist
    cursor.execute('create database if not exists ' +
                   current_app.config['DATABASE'])
    # select database for use
    g.db.select_db(current_app.config['DATABASE'])


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=current_app.config['MYSQL_HOST'],
                               user=current_app.config['MYSQL_USERNAME'],
                               password=current_app.config['MYSQL_PASSWORD'])
        init_db()
        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
