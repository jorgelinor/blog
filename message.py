from google.appengine.ext import db

class Message(db.Model):
	submitter = db.StringProperty(required=True)
	destination = db.StringProperty(required=True)
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)