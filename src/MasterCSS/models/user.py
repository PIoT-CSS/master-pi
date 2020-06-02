"""
userModel.py contains model for user and database logic.
"""

import os
from flask_login import (
    UserMixin
)
from MasterCSS.database import db, ma
from flask import Flask


class UserSchema(ma.Schema):
    """
    This UserSchema stores the meta and schema of user.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """

    def __init__(self, strict=True, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("ID", "FirstName", "LastName", "Username", "Email",
                  "Password", "PhoneNumber", "UserType", "MacAddress")


class User(db.Model, UserMixin):
    """
    User model class represents a user in the database.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """
    __tablename__ = "User"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.Text, nullable=False)
    LastName = db.Column(db.Text, nullable=False)
    Username = db.Column(db.Text, nullable=False)
    Email = db.Column(db.Text, nullable=False)
    Password = db.Column(db.Text, nullable=False)
    PhoneNumber = db.Column(db.Text, nullable=False)
    UserType = db.Column(db.Text, nullable=False)
    MacAddress = db.Column(db.Text, nullable=True)

    def __init__(self, FirstName, LastName, Username, Email, Password,
                 PhoneNumber, UserType, ID=None, MacAddress=None):
        self.ID = ID
        self.FirstName = FirstName
        self.LastName = LastName
        self.Username = Username
        self.Email = Email
        self.Password = Password
        self.PhoneNumber = PhoneNumber
        self.UserType = UserType
        self.MacAddress = MacAddress

    def get_id(self):
        """
        Return the login ID for flask_login.

        :return: login identity number
        :rtype: int
        """
        return (self.ID)
