import os
import time
from flask import Flask, send_file
from flask_restful import Api
import csv
from celery.result import AsyncResult
from celery_background.celery_worker import make_celery
from config.config import LocalDevelopmentConfig
from models.database import db
from routes.api_routes import api_routes
from routes.manager_api_routes import manager
from routes.routes import routes
from routes.user_api_routes import user
from json import dumps
from httplib2 import Http
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from jinja2 import Template

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@glimpse.com"
SENDER_PASSWORD = ""


def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True


def create_app():
    app_create = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Staring Local Development")
        app_create.config.update(
            CELERY_BROKER_URL='redis://localhost:6379',
            CELERY_RESULT_BACKEND='redis://localhost:6379'
        )
        celery_app = make_celery(app_create)
        app_create.config.from_object(LocalDevelopmentConfig)
    db.init_app(app_create)
    api_create = Api(app_create)

    app_create.app_context().push()
    return app_create, api_create, celery_app


app, api, celery = create_app()


@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b


@celery.task()
def generate_csv():
    time.sleep(6)
    fields = ['Name', 'Branch', 'Year', 'CGPA']
    rows = [['Nikhil', 'COE', '2', '9.0'],
            ['Sanchit', 'COE', '2', '9.1'],
            ['Aditya', 'IT', '2', '9.3'],
            ['Sagar', 'SE', '1', '9.5'],
            ['Prateek', 'MCE', '3', '7.8'],
            ['Sahil', 'EP', '2', '9.1']]

    with open('static/data.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    return 'Job Started'


@app.route("/trigger-celery")
def trigger_celery():
    res = generate_csv.delay()
    return {
        "Task_ID": res.id,
        "Task_State": res.state,
        "Task_Status": res.status
    }


@app.route("/status/<int:id>")
def check_status(id):
    res = AsyncResult(id)
    return {
        "Task_ID": res.id,
        "Task_State": res.state,
        "Task_Status": res.status
    }


@app.route("/download")
def download():
    return send_file("static/data.csv")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, add_together.s(9, 7), name='add every 10')
    sender.add_periodic_task(30.0, send_reminder.s(), name='add every 30')
    sender.add_periodic_task(30.0, send_email.s(), name ="email reminder")


@celery.task
def send_reminder():
    """
    Google
    Chat
    incoming
    webhook
    quickstart.
    """
    url = "https://chat.googleapis.com/v1/spaces/AAAAqavgIj0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MCZkFMJmGgsGOhRYSRmG9oW_76LpNbAlNxdocu7zx_k"
    app_message = {
        'text': 'Reminder to Login to Grocery Store'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)
    return "Reminder will send soon"


@celery.task
def send_reminder():
    send_email(
        to_address="dummy@gmail.com",
        subject="Not Buying Today",
        message="Please buy today ",

    )
    return "Email should aarive in inbox shortly"


app.register_blueprint(routes)
app.register_blueprint(user, url_prefix='/api')
app.register_blueprint(manager, url_prefix='/api')
app.register_blueprint(api_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
