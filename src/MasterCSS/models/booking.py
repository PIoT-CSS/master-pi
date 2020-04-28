"""
booking.py contains db model for booking.
"""
import os
from flask import Flask
from MasterCSS.cli import db, ma


class BookingSchema(ma.Schema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        fields = ("ID", "UserID", "DateTimeBooked", "DateTimeStart",
                  "DateTimeEnd", "Cost", "PickupCoordinates", "DropCoordinates",
                  "Distance", "Status")


class Booking(db.Model):
    __tablename__ = "Booking"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, nullable=False)
    DateTimeBooked = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False)
    DateTimeStart = db.Column(db.DateTime, nullable=False)
    DateTimeEnd = db.Column(db.DateTime, nullable=False)
    Cost = db.Column(db.Float, nullable=False)
    PickupCoordinates = db.Column(db.Text, nullable=False)
    DropCoordinates = db.Column(db.Text, nullable=False)
    Distance = db.Column(db.Text, nullable=False)
    Status = db.Column(db.Text, nullable=False)
