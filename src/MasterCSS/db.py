"""
db.py module contains database setup.
"""
from flask import current_app, g
import pymysql


def init():
    g.db = pymysql.connect(host=current_app.config['MYSQL_HOST'],
                            user=current_app.config['MYSQL_USERNAME'],
                            password=current_app.config['MYSQL_PASSWORD'])
    # obtain database cursor
    cursor = g.db.cursor()
    # # initialise database if not exist
    cursor.execute("create database if not exists " +
                    current_app.config['DATABASE'] + ";")
    g.db.select_db(current_app.config['DATABASE'])
    # create user table, can move into its function?
    cursor.execute("""
            create table if not exists User (
                id int not null auto_increment,
                firstname text not null,
                lastname text not null,
                username text not null,
                email text not null,
                password text not null,
                phonenumber text not null,
                usertype text not null, 
                constraint PK_User primary key (id)
            );""")
    g.db.commit()


def get_db():
    if 'db' not in g:
        init()
    return g.db


def close(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
