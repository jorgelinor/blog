import handler
import hashlib
from google.appengine.ext import db

class Profile(handler.Handler):
	def get(self):
		user = db.GqlQuery("select * from User where user_id='"+self.request.cookies.get('user_id').split("|")[0]+"'").fetch(1)
		if self.request.cookies.get("user_id") == "" or not self.request.cookies.get("user_id"):
			self.redirect("/login")
		else:
			if user:
				self.render("profile.html", user=user[0],desc=user[0].user_desc)
			else:
				self.redirect("/login")