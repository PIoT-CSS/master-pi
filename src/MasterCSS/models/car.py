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
        fields = ("ID", "Make", "Seats", "BodyType", "Coordinates",
                  "Colour", "CostPerHour", "FuelType", "RentalID")


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
    RentalID = db.Column(db.Integer)

    def __init__(self, Make, Seats, BodyType, Coordinates,
                 Colour, CostPerHour, FuelType, RentalID, ID=None):
        self.ID = ID
        self.Make = Make
        self.Seats = Seats
        self.BodyType = BodyType
        self.Coordinates = Coordinates
        self.Colour = Colour
        self.CostPerHour = CostPerHour
        self.FuelType = FuelType
        self.RentalID = RentalID
