"""
car.py contains db model for car.
"""
import os
from flask import Flask
from MasterCSS.database import db, ma

LONGTEXT_LENGTH = 4294000000


class CarSchema(ma.Schema):
    """
    This CarSchema stores the meta and schema of a car.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """

    def __init__(self, strict=True, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("ID", "Make", "Seats", "BodyType", "HomeCoordinates",
                  "Coordinates", "Colour", "CostPerHour", "FuelType",
                  "TotalDistance", "NumberPlate", "CurrentBookingID",
                  "AgentID", "Image")


class Car(db.Model):
    """
    Car model class represents a car in the database.
    A car has Booking as its foreign key.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """
    __tablename__ = "Car"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Make = db.Column(db.Text, nullable=False)
    Seats = db.Column(db.Integer, nullable=False)
    BodyType = db.Column(db.Text, nullable=False)
    Coordinates = db.Column(db.Text, nullable=False)
    HomeCoordinates = db.Column(db.Text, nullable=False)
    Colour = db.Column(db.Text, nullable=False)
    CostPerHour = db.Column(db.Float, nullable=False)
    FuelType = db.Column(db.Text, nullable=False)
    TotalDistance = db.Column(db.Float, nullable=False)
    NumberPlate = db.Column(db.Text, nullable=False)
    CurrentBookingID = db.Column(db.Integer)
    AgentID = db.Column(db.Text, nullable=False)
    Image = db.Column(db.Text(LONGTEXT_LENGTH), nullable=False)

    def __init__(self, Make, Seats, BodyType, Coordinates, HomeCoordinates,
                 Colour, CostPerHour, FuelType, TotalDistance, NumberPlate,
                 AgentID, Image, CurrentBookingID=None, ID=None):
        self.ID = ID
        self.Make = Make
        self.Seats = Seats
        self.BodyType = BodyType
        self.Coordinates = Coordinates
        self.HomeCoordinates = HomeCoordinates
        self.Colour = Colour
        self.CostPerHour = CostPerHour
        self.FuelType = FuelType
        self.TotalDistance = TotalDistance
        self.NumberPlate = NumberPlate
        self.CurrentBookingID = CurrentBookingID
        self.AgentID = AgentID
        self.Image = Image
