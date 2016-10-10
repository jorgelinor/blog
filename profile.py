import handler
import hashlib
from google.appengine.ext import db

class Profile(handler.Handler):
	def get(self):
		user = db.GqlQuery("select * from User where user_id='"+self.request.cookies.get('user_id').split("|")[0]+"'").fetch(1)
		if not self.request.get("u"):
			if self.request.cookies.get("user_id") == "" or not self.request.cookies.get("user_id"):
				self.redirect("/login")
			else:
				if user:
					self.render("profile.html", user=user[0],desc=user[0].user_desc,modificable=True)
				else:
					self.redirect("/login")
		else:
			user = db.GqlQuery("select * from User where user_id='"+self.request.get("u")+"'").fetch(1)
			if user:
				if self.request.get("u") == self.request.cookies.get("user_id").split("|")[0]:
					self.redirect("/profile")
				else:
					self.render("profile.html", user=user[0],desc=user[0].user_desc)
			else:
				self.write("Perfil no encontrado")
