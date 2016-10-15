from google.appengine.ext import db

class Comment(db.Model):
	title = db.TextProperty(required=True)
	content = db.TextProperty(required=True)
	post = db.StringProperty(required=True)
	submitter = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	reported = db.BooleanProperty(required=True)
	razon = db.ListProperty(str,required=True)