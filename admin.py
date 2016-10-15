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
			if user.user_type == "admin":
				self.render("admin.html", pagename="Administracion",user=user)
			else:
				self.redirect("/")
		else:
			self.redirect("/login")

class PostRequest(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.user_type == "admin":
				posts = db.GqlQuery("select * from Post where modificable='pending'")
				if self.request.get("post"):
					post = Post.get_by_id(int(self.request.get("post")))
					if post:
						if self.request.get("action"):
							if self.request.get("action") == "accept_request":
								post.modificable = 'True'
								post.put()
								self.redirect("/admin/post_requests")
							else:
								if self.request.get("action") == "deny_request":
									post.modificable = "False"
									post.put()
									self.redirect("/admin/post_requests")
								else:
									self.redirect("/admin/post_requests")
						else:
							self.redirect("/admin/post_requests")
					else:
						self.redirect("/admin/post_requests")
				else:
					if posts:
						posts = list(posts)
						self.render("page.html", user=user.user_id,posts=posts,pagename="Edicion de publicaciones")
					else:
						self.write("No hay posts pendientes por el momento")
			else:
				self.redirect("/")
		else:
			self.redirect("/login")
class Users(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.user_type == "admin":
				users = db.GqlQuery("select * from User")
				if self.request.get("u"):
					profile = db.GqlQuery("select * from User where user_id='"+self.request.get("u")+"'").fetch(1)[0]
					if profile:
						if self.request.get("action"):
							if self.request.get("action") == "ascend":
								profile.user_type = "admin"
							if self.request.get("action") == "descend":
								profile.user_type = "user"
							if self.request.get("action") == "ban_posting":
								profile.banned_from_posting = True
							if self.request.get("action") == "allow_posting":
								profile.banned_from_posting = False
							if self.request.get("action") == "ban_comments":
								profile.banned_from_comments = True
							if self.request.get("action") == "allow_comments":
								profile.banned_from_comments = False
							profile.put()
							self.redirect("/admin/users")
						else:
							self.redirect("/admin/users")
					else:
						self.redirect("/admin/users")
				else:
					if users:
						users = list(users)
						self.render("users.html",users=users,pagename="Panel de usuarios", user=user)
			else:
				self.redirect("/")
		else:
			self.redirect("/login")






