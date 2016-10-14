from google.appengine.ext import db
import handler
import hashlib
from user import User
from post import Post

class Admin(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.type == "admin":
				self.render("admin.html")
			else:
				self.error(502)
		else:
			self.redirect("/")

class PostRequest(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.user_type == "admin":
				posts = db.GqlQuery("select * from Post where modificable='pending'")
				if posts:
					posts = list(posts)
					self.render("page.html", user=user.user_id,posts=posts)
				else:
					self.write("No hay posts pendientes por el momento")
			else:
				self.redirect("/")
		else:
			self.redirect("/login")
class AcceptRequest(handler.Handler):
	def get(self,post):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.user_type == "admin":
				post = Post.get_by_id(int(post))
				if post:
					post.modificable = 'True'
					post.put()
					self.redirect("/admin/post_requests")
				else:
					self.write("No hay posts pendientes por el momento")
			else:
				self.redirect("/")
		else:
			self.redirect("/login")




