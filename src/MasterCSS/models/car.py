"""
car.py contains db model for car.
"""
import os
from flask import Flask
from MasterCSS.cli import db, ma


class CarSchema(ma.Schema):
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        fields = ("ID", "Make", "Seats", "BodyType", "Coordinates", "Colour",
                  "CostPerHour", "FuelType", "TotalDistance", 
                  "NumberPlate", "CurrentBookingID")


class Car(db.Model):
    __tablename__ = "Car"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Make = db.Column(db.Text, nullable=False)
    Seats = db.Column(db.Integer, nullable=False)
    BodyType = db.Column(db.Text, nullable=False)
    Coordinates = db.Column(db.Text, nullable=False)
    Colour = db.Column(db.Text, nullable=False)
    CostPerHour = db.Column(db.Float, nullable=False)
    FuelType = db.Column(db.Text, nullable=False)
    TotalDistance = db.Column(db.Float, nullable=False)
    NumberPlate = db.Column(db.Text, nullable=False)
    CurrentBookingID = db.Column(db.Integer, db.ForeignKey('Booking.ID'))
    Bookings = db.relationship('Booking', backref='Car', lazy=True)

    def __init__(self, Make, Seats, BodyType, Coordinates,
                 Colour, CostPerHour, FuelType, TotalDistance, NumberPlate, 
                 CurrentBookingID, ID=None):
        self.ID = ID
        self.Make = Make
        self.Seats = Seats
        self.BodyType = BodyType
        self.Coordinates = Coordinates
        self.Colour = Colour
        self.CostPerHour = CostPerHour
        self.FuelType = FuelType
        self.TotalDistance = TotalDistance
        self.NumberPlate = NumberPlate
        self.CurrentBookingID = CurrentBookingID
