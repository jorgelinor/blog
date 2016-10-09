from google.appengine.ext import db
import re

class User(db.Model):
    user_id = db.StringProperty(required=True)
    user_pw = db.StringProperty(required=True)
    user_mail = db.StringProperty(required=True)
    user_tel = db.StringProperty(required=False)
    user_date = db.StringProperty(required=False)
    user_desc = db.TextProperty(required=False)
