#clase de salida

import handler

class Logout(handler.Handler):
	def get(self):
		self.delete_data('user_'+self.request.cookies.get('user_id').split('|')[0])
		self.response.headers.add_header('Set-Cookie','user_id=;Path=/')
		self.redirect('/')