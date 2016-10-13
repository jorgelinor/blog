import handler
from post import Post
import hashlib
from user import User
import comment
from google.appengine.ext import db


class Permalink(handler.Handler):
	def get(self,link):
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user))
			if user:
				user = user.user_id
		else:
			self.redirect("/login")
		post = Post.get_by_id(int(link[:]))
		if post:
			submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'")
			submitter = list(submitter)
			if len(submitter) < 1:
				post.submitter = post.submitter+"|False"
			else:
				if post.submitter == user:
					post.submitter = "ti"
				else:
					post.submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'").fetch(1)[0].displayName+"|True"
			comments = db.GqlQuery("select * from Comment where post='"+link+"' order by created desc")
			comments = list(comments)
			user = self.request.cookies.get("user_id")
			if user and hashlib.sha256(user.split("|")[0]).hexdigest() == user.split("|")[1]:
				user = user.split("|")[0]
				user = User.get_by_id(int(user))
				if user:
					user = user.user_id
				else:
					self.redirect("/login")
			else:
				self.redirect("/login")
			for e in comments:
				submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'")
				submitter = list(submitter)
				if len(submitter) < 1:
					e.submitter = e.submitter+"|False"
				else:
					if e.submitter == user:
						e.submitter = "ti"
					else:
						e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName+"|True"
			self.render('permalink.html',post=post,user=user,comments=comments)
		else:
			self.redirect('/')

class Comment(handler.Handler):
	def get(self,link):
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user))
			if user:
				user = user.user_id
		else:
			self.redirect("/login")
		post = Post.get_by_id(int(link[:]))
		submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'")
		submitter = list(submitter)
		if len(submitter) < 1:
			post.submitter = post.submitter+"|False"
		else:
			if post.submitter == user:
				post.submitter = "ti"
			else:
				post.submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'").fetch(1)[0].displayName+"|True"
		if post:
			comments = db.GqlQuery("select * from Comment where post='"+link+"' order by created desc")
			comments = list(comments)
			user = self.request.cookies.get("user_id").split("|")[0]
			if user:
				user = User.get_by_id(int(user)).user_id
			for e in comments:
				submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'")
				submitter = list(submitter)
				if len(submitter) < 1:
					e.submitter = e.submitter+"|False"
				else:
					if e.submitter == user:
						e.submitter = "ti"
					else:
						e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName+"|True"
			self.render('permalink.html',post=post,user=user,newcomment=True,comments=comments)
		else:
			self.redirect('/')
	def post(self,link):
		submitter = self.request.cookies.get('user_id').split('|')[0]
		submitter = User.get_by_id(int(submitter))
		if submitter.banned_from_comments == True:
			self.redirect("/")
		content = self.request.get("content")
		comments = db.GqlQuery("select * from Comment where post='"+link+"'")
		post_title = Post.get_by_id(int(link)).title
		if len(content) < 1:
			self.redirect('/'+link)
		else:
			com = comment.Comment(submitter=submitter.user_id,content=content,post=link,title="Comentario #"+str(len(list(comments))+1)+" en "+post_title)
			com.put()
			self.redirect("/"+link)
class EditComment(handler.Handler):
	def get(self, link):
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			post = Post.get_by_id(int(link))
			if post:
				if self.request.get("c"):
					if comment.Comment.get_by_id(int(self.request.get("c"))):
						com = comment.Comment.get_by_id(int(self.request.get("c")))
						if com:
							if int(com.post) == post.key().id():
								comments = db.GqlQuery("select * from Comment where post='"+link+"' order by created desc")
								comments = list(comments)
								for e in comments:
									submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'")
									submitter = list(submitter)
									if len(submitter) < 1:
										e.submitter = e.submitter+"|False"
									else:
										if e.submitter == user.user_id:
											e.submitter = "ti"
										else:
											e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName+"|True"
								post.submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'").fetch(1)[0].displayName
								self.render("permalink.html",user=user.user_id,comments=comments,post=post,editcomment=True,comment=com)
							else:
								self.write("Este comentario no pertenece a este Post.")
						else:
							self.write("Comentario no encontrado.")
					else:
						self.redirect("/"+link)
				else:
					self.redirect("/"+link)
			else:
				self.redirect("/")
		else:
			self.redirect("/login")
	def post(self,link):
		content = self.request.get("content")
		if len(content) < 1:
			self.redirect("/"+link)
		else:
			com = comment.Comment.get_by_id(int(self.request.get("c")))
			com.content = content
			com.put()
			self.redirect("/"+link)
