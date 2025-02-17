"""
issue.py contains issue controllers.
"""
from ast import literal_eval as make_tuple
from MasterCSS.constant import Constant
import os
from MasterCSS.models.car import Car
from MasterCSS.models.issue import Issue
from MasterCSS.models.user import User
from MasterCSS.database import db
import requests
import json
from flask import (
    request,
    url_for,
    Blueprint,
    redirect,
    render_template,
    session,
    current_app
)
from flask_login import (
    current_user,
    login_required
)

# Setup Blueprint
controllers = Blueprint("issue_controllers", __name__)

ISSUE_API_URL = '/issue'


@controllers.route(ISSUE_API_URL, methods=['GET'])
@login_required
def view_all_issues():
    """
    Renders all the issues for admin users to see.

    :return: viewall template that renders all the issues.
    :rtype: render_template
    """
    if current_user.UserType == "ADMIN":
        # Obtain all the issue entries from the db.
        issues = db.session.query(Issue).all()
        return render_template("admin/issues/viewall.html", 
            issues=issues)
    else:
        return render_template("errors/401.html"), 401


@controllers.route(ISSUE_API_URL + '/pending', methods=['GET'])
@login_required
def view_pending():
    """
    Renders all pending issues for engineers to see.

    :return: viewall template that renders all pending issues.
    :rtype: render_template
    """
    if current_user.UserType == "ENGINEER":
        # Obtain all the pending issues from the db.
        issues = db.session.query(Issue).filter_by(Status=Issue.PENDING)
        return render_template("engineer/viewpending.html", 
            issues=issues)
    else:
        return render_template("errors/401.html"), 401


@controllers.route(ISSUE_API_URL + '/taken', methods=['GET'])
@login_required
def view_taken():
    """
    View all the issues that an engineer has resolved

    :return: viewtaken template that renders issues that hold a user id that matches with a logged in engineer.
    :rtype: render_template
    """
    if current_user.UserType == "ENGINEER":
        # Obtain all the issues taken by the engineer entries from the db.
        issues = db.session.query(Issue).filter_by(UserID=current_user.ID)
        return render_template("engineer/viewtaken.html", issues=issues)
    else:
        return render_template("errors/401.html"), 401


@controllers.route(ISSUE_API_URL + '/view/<int:id>', methods=['GET'])
@login_required
def view_issue(id):
    """
    View a partiuclar issue

    :param id: issue id.
    :type id: int
    :return: renders template to view issue details
    :rtype: render_template
    """
    issue = db.session.query(Issue).get(id)
    car = db.session.query(Car).get(issue.CarID)
    usertype = current_user.UserType
    if usertype == "ADMIN" or usertype == "ENGINEER":
        return render_template("engineer/view.html", issue=issue,
            car=car, car_coordinates=Constant.CAR_COORDINATES)
    else:
        return render_template("errors/401.html"), 401


@controllers.route(ISSUE_API_URL + '/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create_new_issue(id):
    """
    GET returns template of form to create issue, POST to 
    add issue to the db

    :param id: id of car
    :type id: int
    :return: renders either a form or viewall issues template.
    :rtype: render_template
    """
    car = db.session.query(Car).get(id)
    if current_user.UserType == "ADMIN":
        if request.method == 'GET':
            return render_template("admin/issues/add.html", car=car,
                car_coordinates=Constant.CAR_COORDINATES)
        elif request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            carid = car.ID
            status = 0

            issue = Issue(carid, title, description, status)
            # add issue to db.
            db.session.add(issue)
            db.session.commit()

            # send request to pb api to send notification
            notif_body = "Issue ID:{}, Description:{}".format(
                issue.ID, issue.Description)
            notif_title = "New Issue for car {}, {}".format(
                car.ID, issue.Title)

            if not current_app.config["TESTING"]:
                send_notification(notif_title, notif_body)

            return redirect(url_for('issue_controllers.view_all_issues'))
    else:
        return render_template("errors/401.html"), 401


@controllers.route(ISSUE_API_URL + '/resolve/<int:id>', methods=['GET'])
@login_required
def resolve_issue(id):
    """
    Resolves a particular issue, changing the issue status

    :param id: issue id
    :type id: int
    :return: redirects to view taken controller if logged in user is an engineer, if logged in user is an admin redirects to view all issues controller.
    :rtype: redirect
    """
    issue = db.session.query(Issue).get(id)
    usertype = current_user.UserType
    if usertype == "ADMIN" or usertype == "ENGINEER":
            issue.Status = Issue.RESOLVED
            issue.UserID = current_user.ID
            db.session.commit()
            if usertype == "ADMIN":
                return redirect(url_for('issue_controllers.view_all_issues'))
            elif usertype == "ENGINEER":
                return redirect(url_for('issue_controllers.view_taken'))
    else:
        return render_template("errors/401.html"), 401


def handle_resolve_issue(eng_id, issue_id):
    """
    Handles payload from AP containing eng_id, issue_id
    that indicates the issue has been fixed by an engineer.

    :param eng_id: user id that belongs to an engineer
    :type eng_id: int
    :param issue_id: issue id belongs to the issue being resolved
    :type issue_id: int
    """
    user = db.session.query(User).get(int(eng_id))
    if user == None:
        print("[AP Issue Resolver] User/Engineer {} doesn't exist!"
            .format(eng_id))
    elif user.UserType != "ENGINEER":
        print("[AP Issue Resolver] User {} isn't an engineer!"
            .format(eng_id))
    issue = db.session.query(Issue).get(int(issue_id))
    if issue == None:
        print("[AP Issue Resolver/ENG {}] Issue {} doesn't exist!"
            .format(eng_id, issue_id))
    elif issue.Status == Issue.RESOLVED:
        print("[AP Issue Resolver/ENG {}] Issue {} has already been resolved!"
            .format(eng_id, issue_id))
    else:
        issue.UserID = int(eng_id)
        issue.Status = Issue.RESOLVED
        db.session.commit()
        print("[AP Issue Resolver/ENG {}] Issue {} has been marked as resolved!"
            .format(eng_id, issue_id))

def send_notification(title, body):
    """
    sends a pb notification to all of the engineer 
    devices that were registered in pushbullet account.

    :param title: title of the notification
    :type title: string
    :param body: body of the notification
    :type body: string
    :return: if false then the token is not found within .env file
    :rtype: boolean
    """
    token = os.getenv('PB_TOKEN')
    if token is None:
        print('No PushBullet API Token found, notification will not be sent.')
        return False
    endpoint='https://api.pushbullet.com/v2/pushes'
    content={"type": "note", "title": title, "body": body}

    response=requests.post(endpoint, data=json.dumps(content),
                                headers={'Access-Token': token,
                                        'Content-Type': 'application/json'})
