#clase de salida

import handler

class Logout(handler.Handler):
	def get(self):
		self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1],actualizar=True)
		self.response.headers.add_header('Set-Cookie','user_id=;Path=/')
		self.redirect('/')
