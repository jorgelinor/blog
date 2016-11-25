#clase de salida

import handler

class Logout(handler.Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie','user_id=;Path=/')
		self.response.headers.add_header('Set-Cookie','limit=;Path=/')
		self.redirect('/posts/news')
