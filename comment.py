from google.appengine.ext import db

class Comment(db.Model):
	submitter = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateProperty(auto_now_add=True)