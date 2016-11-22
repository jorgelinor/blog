from google.appengine.ext import db
import handler

class Message(db.Model):
	submitter = db.StringProperty(required=True)
	destination = db.StringProperty(required=True)
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)

	@classmethod
	def by_destination(self,name):
		m = handler.Handler().get_data('Message','list')
		return m