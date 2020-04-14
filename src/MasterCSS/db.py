from flask import current_app, g
import pymysql


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=current_app.config['MYSQL_HOST'],
                               user=current_app.config['MYSQL_USERNAME'],
                               password=current_app.config['MYSQL_PASSWORD'],
                               db=current_app.config['DATABASE'])
        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
