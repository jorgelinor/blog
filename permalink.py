import handler
from post import Post
import hashlib
from user import User
import comment
from google.appengine.ext import db


class Permalink(handler.Handler):
	def get(self,link):
		messages = None
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user))
			if not user:
				self.redirect("/login")
		if not user or user == '' or user == None:
			self.redirect("/login")
		else:
			post = Post.get_by_id(int(link[:]))
			if post:
				submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'")
				submitter = list(submitter)
				if len(submitter) < 1:
					post.submitter = post.submitter+"|False"
				else:
					if post.submitter == user.user_id:
						post.submitter = "ti"
					else:
						post.submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'").fetch(1)[0].displayName+"|True"
				comments = db.GqlQuery("select * from Comment where post='"+link+"' order by created desc")
				comments = list(comments)
				user = self.request.cookies.get("user_id") #aqui habia error
				if user and hashlib.sha256(user.split("|")[0]).hexdigest() == user.split("|")[1]:
					user = user.split("|")[0]
					user = User.get_by_id(int(user))
					if not user:
						self.redirect("/login")
				else:
					self.redirect("/login")
				messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
				if messages:
					messages = list(messages)
					for e in messages:
						if e.submitter != "Administracion":
							e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
					for e in comments:
						submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'")
						submitter = list(submitter)
						if len(submitter) < 1:
							e.submitter = e.submitter+"|False"
						else:
							if e.submitter == user.user_id:
								e.submitter = "ti"
							else:
								e.submitter = list(db.GqlQuery("select * from User where user_id='"+e.submitter+"'"))[0].displayName+"|True"
					self.render('permalink.html',pagename='Post',post=post,user=user,comments=comments,recent_msg=messages)
				else:
					self.redirect('/')
			else:
				self.redirect("/login")

class Comment(handler.Handler):
	def get(self,link):
		messages = None
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user))
			if user:
				user = user
			if user.banned_from_comments == True:
				self.redirect("/")
		else:
			self.redirect("/login")
		post = Post.get_by_id(int(link))
		submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'")
		submitter = list(submitter)
		if len(submitter) < 1:
			post.submitter = post.submitter+"|False"
		else:
			if post.submitter == user.user_id:
				post.submitter = "ti"
			else:
				post.submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'").fetch(1)[0].displayName+"|True"
		if post:
			comments = db.GqlQuery("select * from Comment where post='"+link+"' order by created desc")
			comments = list(comments)
			user = self.request.cookies.get("user_id").split("|")[0]
			if user:
				user = User.get_by_id(int(user))
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
			if messages:
				messages = list(messages)
				for e in messages:
					if e.submitter != "Administracion":
						e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
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
			self.render('permalink.html',pagename='Comentar',post=post,user=user,newcomment=True,comments=comments,recent_msg=messages)
		else:
			self.redirect('/')
	def post(self,link):
		submitter = self.request.cookies.get('user_id').split('|')[0]
		submitter = User.get_by_id(int(submitter))
		content = self.request.get("content")
		comments = db.GqlQuery("select * from Comment where post='"+link+"'")
		post_title = Post.get_by_id(int(link)).title
		if len(content) < 1:
			self.redirect('/'+link)
		else:
			com = comment.Comment(submitter=submitter.user_id,content=content,post=link,reported=False,title="Comentario #"+str(len(list(comments))+1)+" en "+post_title)
			com.put()
			self.redirect("/"+link)

class EditPost(handler.Handler):
	def get(self,link):
		messages = None
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user))
			if user:
				user = user
		else:
			self.redirect("/login")
		messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
		if messages:
			messages = list(messages)
			for e in messages:
				if e.submitter != "Administracion":
					e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
		post = Post.get_by_id(int(link))
		submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'")
		submitter = list(submitter)
		if len(submitter) > 0:
			if post.submitter == user.user_id:
				if post.modificable == 'True':
					self.render('ascii.html',user=user,pagename='Editar post',title=post.title,post=post.post,error='',editable=True,recent_msg=messages)
				else:
					self.redirect("/"+str(post.key().id())+'/_editrequest')
			else:
				self.write("<a href='/"+str(post.key().id())+"'>Este no es tu post!</a>")
		else:
			self.write("<a href='/"+str(post.key().id())+"'>Este post no tiene duenio</a>")

	def post(self,link):
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user))
			if user:
				user = user
		post = Post.get_by_id(int(link))
		content = self.request.get('content')
		title = self.request.get('subject')
		if title and post:
			post.title = title
			post.post = content
			post.modificable = "False"
			post.put()
			self.redirect('/'+str(post.key().id()))
		else:
			error = 'we need more...'
			self.render('ascii.html',pagename='Editar post',user=user,title=title,post=content,error=error,editable=True)

class EditComment(handler.Handler):
	def get(self, link):
		messages = None
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			post = Post.get_by_id(int(link))
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
			if messages:
				messages = list(messages)
				for e in messages:
					if e.submitter != "Administracion":
						e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
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
								self.render("permalink.html",pagename='Editar comentario',user=user,comments=comments,post=post,editcomment=True,comment=com,recent_msg=messages)
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

class ReportComment(handler.Handler):
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
								self.render("permalink.html",pagename='Reportar comentario',user=user,comments=comments,post=post,reportcomment=True,comment=com)
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
		razon = self.request.get("razon")
		if len(razon) < 1:
			self.redirect("/"+link)
		else:
			com = comment.Comment.get_by_id(int(self.request.get("c")))
			com.razon = com.razon+[razon]
			com.reported = True
			com.put()
			self.redirect("/"+link)

class EditRequest(handler.Handler):
	def get(self,link):
		messages = None
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1] and User.get_by_id(int(user.split('|')[0])):
			user = User.get_by_id(int(user.split('|')[0]))
			post = Post.get_by_id(int(link))
			if post:
				if post.submitter == user.user_id:
					if Post.get_by_id(int(link)).modificable == 'False':
						messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
						if messages:
							messages = list(messages)
							for e in messages:
								if e.submitter != "Administracion":
									e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
						self.render('editrequest.html',user=user,pagename='Permiso para editar',post=post,recent_msg=messages)
					else:
						self.redirect('/'+link)
				else:
					self.redirect('/'+link)
			else:
				self.redirect('/')
		else:
			self.redirect('/login')
	def post(self,link):
		razon = self.request.get('razon')
		if razon:
			post = Post.get_by_id(int(link))
			post.modificable = 'pending'
			post.razon = razon
			post.put()
		self.redirect('/'+link)

