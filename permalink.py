import handler
from post import Post
import hashlib
from user import User
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
			user = None
		post = Post.get_by_id(int(link[1:]))
		submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'")
		submitter = list(submitter)
		if len(submitter) < 1:
			post.submitter = "Este usuario se murio de SIDA"
		else:
			post.submitter = db.GqlQuery("select * from User where user_id='"+post.submitter+"'").fetch(1)[0].displayName
		if post:
			self.render('permalink.html',post=post,user=user)
		else:
			self.redirect('/')