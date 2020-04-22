from flask_login import (
    UserMixin
)
import os
import hashlib, uuid
from base64 import b64encode, b64decode
import MasterCSS.db as Db

# define salt length for hashing purposes
SALT_LENGTH = 32

# define database cursor constants
FIRST_ROW = 0

# define database columns
ID = 0
FIRST_NAME = 1
LAST_NAME = 2
USERNAME = 3
EMAIL = 4
PASSWORD = 5
PHONE_NUMBER = 6
USER_TYPE = 7

class User(UserMixin):
    def __init__(self, id, first_name, last_name, username, email, password, phone_number, user_type):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.user_type = user_type

    @staticmethod
    def get_total_users():
        db = Db.get_db()
        with db.cursor() as cursor:
            cursor.execute("select count(*) from User;")
            result = cursor.fetchall()
        return int(result[FIRST_ROW][ID])

    @staticmethod
    def register(first_name, last_name, username, email, password, phone_number, user_type):
        db = Db.get_db()
        salt = os.urandom(SALT_LENGTH)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        hashed_password = b64encode(salt + key)
        with db.cursor() as cursor:
            # check if username, email, phonenumber are already taken
            takens = list()
            cursor.execute("select * from User where username = %s;", (username))
            user = cursor.fetchall()
            if cursor.rowcount:
                takens.append("Username")
            cursor.execute("select * from User where email = %s;", (email))
            user = cursor.fetchall()
            if cursor.rowcount:
                takens.append("Email")
            cursor.execute("select * from User where phonenumber = %s;", (phone_number))
            user = cursor.fetchall()
            if cursor.rowcount:
                takens.append("Phone number")
            if len(takens) > 0:
                taken_message = "Taken: "
                for i in range(len(takens)):
                    taken_message = taken_message + takens[i]
                    if i != len(takens) - 1:
                        taken_message = taken_message + ", "
                return None, taken_message
            cursor.execute("insert into User (firstname, lastname, username, email, password, phonenumber, usertype) values (%s, %s, %s, %s, %s, %s, %s);", (first_name, last_name, username, email, hashed_password, phone_number, user_type))
        db.commit()
        return User(User.get_total_users(), first_name, last_name, username, email, hashed_password, phone_number, user_type), None

    @staticmethod
    def login(username, password):
        db = Db.get_db()
        with db.cursor() as cursor:
            cursor.execute("select * from User where username = %s;", (username))
            user = cursor.fetchall()
            if cursor.rowcount:
                salt = (b64decode(user[FIRST_ROW][PASSWORD])[:SALT_LENGTH])
                key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                if key == (b64decode(user[FIRST_ROW][PASSWORD])[SALT_LENGTH:]):
                    return User(user[FIRST_ROW][ID], user[FIRST_ROW][FIRST_NAME], user[FIRST_ROW][LAST_NAME], user[FIRST_ROW][USERNAME], user[FIRST_ROW][EMAIL], user[FIRST_ROW][PASSWORD], user[FIRST_ROW][PHONE_NUMBER], user[FIRST_ROW][USER_TYPE]), None
                else:
                    return None, "Password mismatch!"
            return None, "User not found!"

    @staticmethod
    def get_users():
        db = Db.get_db()
        with db.cursor() as cursor:
            cursor.execute("select * from User;")
            users_result = cursor.fetchall()
        for user in users_result:
            yield User(int(user[ID]), user[FIRST_NAME], user[LAST_NAME], user[USERNAME], user[EMAIL], user[PASSWORD], user[PHONE_NUMBER], user[USER_TYPE])

    @staticmethod
    def get_user(id):
        db = Db.get_db()
        with db.cursor() as cursor:
            cursor.execute("select * from User where id = %s;", (id))
            user = cursor.fetchall()
        return User(int(id), user[FIRST_ROW][FIRST_NAME], user[FIRST_ROW][LAST_NAME], user[FIRST_ROW][USERNAME], user[FIRST_ROW][EMAIL], user[FIRST_ROW][PASSWORD], user[FIRST_ROW][PHONE_NUMBER], user[FIRST_ROW][USER_TYPE])

    @staticmethod
    def delete_user(id):
        db = Db.get_db()
        with db.cursor() as cursor:
            cursor.execute("delete from User where id != %s;", (id))
        db.commit()
