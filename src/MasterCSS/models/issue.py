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
    UserID = db.Column(db.Integer, db.ForeignKey('User.ID'))
    CarID = db.Column(db.Integer, db.ForeignKey('Car.ID'), nullable=True)
    Title = db.Column(db.Text, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.Integer, nullable=False)

    # Issue status
    PENDING = 0
    ACTIVE = 1
    RESOLVED = 2

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
        elif id == Issue.ACTIVE:
            return "Active"
        elif id == Issue.RESOLVED:
            return "Resolved"

    def removeRef(self):
        """
        Removes references to car and user when booking is resolved,
        to prevent errors when admin deletes car/user entries.
        """
        self.CarID = None
        self.UserID = None
