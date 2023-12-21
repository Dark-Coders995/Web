from flask import Flask, render_template, send_file, request, Response
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_cors import CORS

from datetime import datetime, timedelta
from celery.result import AsyncResult

import os, time
from sqlalchemy import func
import requests
from celery.schedules import crontab

from Caches.cache import cache
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template


from config.security import user_datastore,security
from models.models import *
from celery_task.workers import make_celery
from config.config import LocalDevelopmentConfig
from models.database import db
from api.Authentication.loginapi import *
from api.Authentication.signupapi import *
from api.Authentication.adminsignup import *
from api.Authentication.adminlogin import *
from api.Admin.add_category import *
from api.Admin.add_product import *
from api.Admin.edit_category import *
from api.Admin.edit_product import *
from api.Admin.delete_category import *
from api.Admin.delete_product import *


from api.User.posted_category import *
from api.User.posted_products import *
from api.User.getProductDetails import *
from api.User.getcategorydetails import *
from api.User.getavailableproducts import *
from api.User.buy_product import *
from api.User.search import *
from api.User.dashboard import *

from api.Summary.summary import *


import csv
import os
import time
from httplib2 import Http
from json import dumps