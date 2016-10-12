import handler
from post import Post
import hashlib
from user import User


class Permalink(handler.Handler):
	def get(self,link):
		user = self.request.cookies.get('user_id')
		if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
			user = user.split('|')[0]
			user = User.get_by_id(int(user)).user_id
		else:
			user = None
		post = Post.get_by_id(int(link[1:]))
		if post:
			self.render('permalink.html',post=post,user=user)
		else:
			self.redirect('/')