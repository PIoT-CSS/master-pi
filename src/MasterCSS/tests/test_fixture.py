"""
test_fixture.py contains unit testing setup.
"""
import pytest
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from MasterCSS.cli import app, db
from MasterCSS.models.user import User

TEST_DB_NAME = os.getenv("UNIT_TESTING_DATABASE")


@pytest.fixture(scope='module')
def client():
    """
    Configure pytest, Flask app and database for unit testing.
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}? \
        charset=utf8mb4".format(
        os.getenv("MYSQL_USERNAME"),
        os.getenv("MYSQL_PASSWORD"),
        os.getenv("MYSQL_HOST"),
        TEST_DB_NAME
    )
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as c:
            # initialise database
            db.engine.execute("drop database {};".format(TEST_DB_NAME))
            db.engine.execute("create database {};".format(TEST_DB_NAME))
            db.engine.execute("use {};".format(TEST_DB_NAME))
            db.create_all()
            yield c
