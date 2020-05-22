"""
booking.py contains db model for booking.
"""
import os
from flask import Flask
from MasterCSS.database import db, ma


class BookingSchema(ma.Schema):
    """
    This BookingSchema stores the meta and schema of a booking.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """
    def __init__(self, strict=True, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("ID", "UserID", "CarID", "DateTimeBooked", "DateTimeStart",
                  "DateTimeEnd", "Cost", "HomeCoordinates",
                  "Distance", "Status", "CalRef")


class Booking(db.Model):
    """
    Booking model class represents a car in the database.
    A Booking has its Car and User as its foreign keys.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """
    __tablename__ = "Booking"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.ID'), nullable=False)
    CarID = db.Column(db.Integer, db.ForeignKey('Car.ID'), nullable=False)
    DateTimeBooked = db.Column(db.DateTime, nullable=False)
    DateTimeStart = db.Column(db.DateTime, nullable=False)
    DateTimeEnd = db.Column(db.DateTime, nullable=False)
    Cost = db.Column(db.Float, nullable=False)
    HomeCoordinates = db.Column(db.Text, nullable=False)
    Distance = db.Column(db.Float, nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    CalRef = db.Column(db.Text)

    # Booking status identity number
    CANCELED = 3
    INACTIVE = 2
    ACTIVE = 1
    CONFIRMED = 0

    def __init__(self, UserID, CarID, DateTimeBooked, DateTimeStart,
                 DateTimeEnd, Cost, HomeCoordinates,
                 Distance, Status, CalRef=None, ID=None):
        self.ID = ID
        self.UserID = UserID
        self.CarID = CarID
        self.DateTimeBooked = DateTimeBooked
        self.DateTimeStart = DateTimeStart
        self.DateTimeEnd = DateTimeEnd
        self.Cost = Cost
        self.HomeCoordinates = HomeCoordinates
        self.Distance = Distance
        self.Status = Status
        self.CalRef = CalRef

    @staticmethod
    def getStatus(id):
        """
        GET booking status.

        :param id: Identity number of the status
        :type id: int
        :return: Booking status as string.
        :rtype: string
        """
        if id == Booking.ACTIVE:
            return "Active"
        elif id == Booking.INACTIVE:
            return "Inactive"
        elif id == Booking.CONFIRMED:
            return "Confirmed"
        elif id == Booking.CANCELED:
            return "Canceled"
