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
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        fields = ("ID", "FirstName", "LastName", "Username", "Email",
                  "Password", "PhoneNumber", "UserType")


class User(db.Model, UserMixin):
    __tablename__ = "User"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.Text, nullable=False)
    LastName = db.Column(db.Text, nullable=False)
    Username = db.Column(db.Text, nullable=False)
    Email = db.Column(db.Text, nullable=False)
    Password = db.Column(db.Text, nullable=False)
    PhoneNumber = db.Column(db.Text, nullable=False)
    UserType = db.Column(db.Text, nullable=False)

    def __init__(self, FirstName, LastName, Username, Email, Password,
                 PhoneNumber, UserType, ID=None):
        self.ID = ID
        self.FirstName = FirstName
        self.LastName = LastName
        self.Username = Username
        self.Email = Email
        self.Password = Password
        self.PhoneNumber = PhoneNumber
        self.UserType = UserType

    # for flask_login
    def get_id(self):
        return (self.ID)
