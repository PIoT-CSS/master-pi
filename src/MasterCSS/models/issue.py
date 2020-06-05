"""
issue.py contains db model for issue.
"""
import os
from flask import Flask
from MasterCSS.database import db, ma

LONGTEXT_LENGTH = 4294000000


class IssueSchema(ma.Schema):
    """
    This IssueSchema stores the meta and schema of a issue.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """

    def __init__(self, strict=True, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ("ID", "CarID", "UserID", "Title", "Description", "Status")


class Issue(db.Model):
    """
    Issue model class represents a Issue in the database.
    A issue has Booking as its foreign key.
    Refererence: https://flask-marshmallow.readthedocs.io/en/latest/
    """
    __tablename__ = "Issue"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer)
    CarID = db.Column(db.Integer)
    Title = db.Column(db.Text, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.Integer, nullable=False)

    # Issue status
    PENDING = 0
    RESOLVED = 1

    def __init__(self, CarID, Title, Description, Status, ID=None, UserID=None):
        self.ID = ID
        self.UserID = UserID
        self.CarID = CarID
        self.Title = Title
        self.Description = Description
        self.Status = Status
    
    @staticmethod
    def getStatus(id):
        """
        GET issue status.

        :param id: Identity number of the status
        :type id: int
        :return: Booking status as string.
        :rtype: string
        """
        if id == Issue.PENDING:
            return "Pending"
        elif id == Issue.RESOLVED:
            return "Resolved"

    def getUser(self):
        """
        Returns the username of user who made the booking

        :return: username of user who made the booking
        :rtype: string
        """
        user = db.session.query(User).get(self.UserID)
        return user
    
    def getCar(self):
        """
        Returns the car associated with the issue.

        :return: car associated with issue.
        :rtype: string
        """
        car = db.session.query(Car).get(self.CarID)
        return car