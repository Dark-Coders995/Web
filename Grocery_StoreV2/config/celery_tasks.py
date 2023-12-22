from application.workers import celery
import datetime
from application.database import db
from application.models import Post, User
import os
from flask import jsonify, make_response, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
import requests
from celery.schedules import crontab

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from jinja2 import Template


@celery.on_after_finalize.connect
def daily_periodic_tasks(sender, **kwargs):
    # UTC Time
    sender.add_periodic_task(crontab(hour=19, minute=59), SendDailyReminder.s(), name="Daily morning")
    sender.add_periodic_task(crontab(hour=19, minute=59, day_of_month=8), SendMonthlyReport.s(),
                             name="1st of every month")


WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAxummSic/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=5iq8Agus9chk4JIdQWfcyW0R15NeXEEh7YJ-liOqabs%3D"


@celery.task()
def SendDailyReminder():
    print("Starting SendDailyReminder Task")

    today = datetime.datetime.utcnow()

    users = db.session.query(User).all()

    for user in users:
        url = WEBHOOK_URL
        data = {
            'text': f"Dear {user.username},\nWe have seen you haven't posted anything today. It's a gentle reminder. We hope you get some time to post today :("}
        r = requests.post(url=url, json=data)


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


def format_message(template_file, lastmonth, data={}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, lastmonth=lastmonth)


def send_monthly_report_email(data, lastmonth):
    message = format_message("monthly_report.html", lastmonth=lastmonth, data=data, )
    send_email(data.email, subject="Monthly Report", message=message)


@celery.task()
def SendMonthlyReport():
    print("Starting SendMonthlyReport Task")

    users = db.session.query(User).all()

    from datetime import datetime
    months = ["Jan", "Feb", "March", "Apr", "May", "jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    currentMonth = datetime.now().month - 1
    currentYear = datetime.now().year
    lastmonth = months[currentMonth - 1] + "-" + str(currentYear)

    for user in users:
        send_monthly_report_email(data=user, lastmonth=lastmonth)

