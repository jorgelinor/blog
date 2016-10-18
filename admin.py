from google.appengine.ext import db
from google.appengine.api import memcache
import handler
import hashlib
from user import User
from post import Post
import time
from message import Message
from comment import Comment

class Admin(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.user_type == "admin":
				messages = self.GetMessage(actualizar=False,persona=user.user_id)
				self.render("admin.html", pagename="Administracion",user=user,recent_msg=messages)
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
				posts = self.get_data("pending_posts",db.GqlQuery("select * from Post where modificable='pending'"))
				if self.request.get("post"):
					post = Post.get_by_id(int(self.request.get("post")))
					if post:
						if self.request.get("action"):
							if self.request.get("action") == "accept_request":
								post.modificable = 'True'
								message = Message(submitter="Administracion", destination=post.submitter, subject="<div style='color:green'><b>PEDIDO ACEPTADO</b></div>", content="Se ha aceptado su pedido para cambiar <a href='/"+self.request.get("post")+"'>este post.</a>")
								message.put()
								post.put()
								self.redirect("/admin/post_requests")
							else:
								if self.request.get("action") == "deny_request":
									post.modificable = "False"
									message = Message(submitter="Administracion", destination=post.submitter, subject="<div style='color:red'><b>PEDIDO DENEGADO</b></div>", content="Se ha denegado su pedido para cambiar <a href='/"+self.request.get("post")+"'>este post.</a>")
									message.put()
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
						messages = self.GetMessage(actualizar=False,persona=user.user_id)
						self.render("page.html", user=user,posts=posts,pagename="Edicion de publicaciones",recent_msg=messages,request=True)
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
				users = memcache.get("users")
				if self.request.get("u"):
					profile = self.get_data(self.request.get("u"),db.GqlQuery("select * from User where user_id='"+self.request.get("u")+"'"))
					if profile:
						changed = False
						if self.request.get("action"):
							if self.request.get("action") == "ascend":
								profile.user_type = "admin"
								changed = True
							if self.request.get("action") == "descend":
								profile.user_type = "user"
								changed = True
							if self.request.get("action") == "ban_posting":
								profile.banned_from_posting = True
								changed = True
							if self.request.get("action") == "allow_posting":
								profile.banned_from_posting = False
								changed = True
							if self.request.get("action") == "ban_comments":
								profile.banned_from_comments = True
								changed = True
							if self.request.get("action") == "allow_comments":
								profile.banned_from_comments = False
								changed = True
							if changed == True:
								profile.put()
							self.redirect("/admin/users")
						else:
							self.redirect("/admin/users")
					else:
						self.redirect("/admin/users")
				else:
					messages = self.GetMessage(actualizar=False,persona=user.user_id)
					self.render("users.html",users=users,pagename="Panel de usuarios", user=user,recent_msg=messages)
			else:
				self.redirect("/")
		else:
			self.redirect("/login")

class Reports(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if user.user_type == "admin":
				messages = self.GetMessage(actualizar=False,persona=user.user_id)
				reported_comments = self.get_data(db.GqlQuery("reported_comments",'select * from Comment where reported=True'))
				self.render('reported.html',user=user,pagename='Reportes',comments=reported_comments,recent_msg=messages)
			else:
				self.redirect('/')
		else:
			self.redirect('/login')
class DeleteComment(handler.Handler):
	def get(self,link):
		comment = Comment.get_by_id(int(link))
		user = self.request.cookies.get('user_id')
		if user:
			if user.split('|')[0].isdigit():
				if hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
					user = User.get_by_id(int(user.split('|')[0]))
					if user.user_type == 'admin':
						post = Post.get_by_id(int(comment.post))
						post.comments -= 1
						post.put()
						db.delete(comment)
						time.sleep(2)
						self.redirect('/admin/reports')
					else:
						self.redirect('/')
				else:
					self.redirect('/login')
			else:
				self.redirect('/login')
		else:
			self.redirect('/login')

class KeepComment(handler.Handler):
	def get(self,link):
		comment = Comment.get_by_id(int(link))
		user = self.request.cookies.get('user_id')
		if user:
			if user.split('|')[0].isdigit():
				if hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
					user = User.get_by_id(int(user.split('|')[0]))
					if user.user_type == 'admin':
						comment.razon = []
						comment.reported = False
						comment.put()
						time.sleep(2)
						self.redirect('/admin/reports')
					else:
						self.redirect('/')
				else:
					self.redirect('/login')
			else:
				self.redirect('/login')
		else:
			self.redirect('/login')