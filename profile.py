import handler
import hashlib
import re
import time
from google.appengine.ext import db
from user import User

class Profile(handler.Handler):
	def get(self):
		user_db = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if not self.request.get("u"):
			if self.request.cookies.get("user_id") == "" or not self.request.cookies.get("user_id"):
				self.redirect("/login")
			else:
				if user_db:
					self.render("profile.html", user=user_db,desc=user_db.user_desc,modificable=True)
				else:
					self.redirect("/login")
		else:
			user = db.GqlQuery("select * from User where user_id='"+self.request.get("u")+"'").fetch(1)
			if user:
				if str(user[0].key().id()) == str(self.request.cookies.get("user_id").split("|")[0]):
					self.redirect("/profile")
				else:
					self.render("profile.html", user=user[0],desc=user[0].user_desc)
			else:
				self.write("Perfil no encontrado")

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if USER_RE.match(username):
        return (True,username)
    else:
        return (False,username)

class EditProfile(handler.Handler):
	def get(self):
		user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		self.render("editprofile.html", user=user,date=user.user_date.split("-"))
	def post(self):
		username = valid_username(self.request.get('username'))
		actual_password = self.request.get('actualpassword')
		tel = self.request.get('tel')
		date = self.request.get('date1')+'-'+self.request.get('date2')+'-'+self.request.get('date3')
		description = self.request.get('description')
		erroruser,errortel,errordesc,errordate,passerror='','','','',''
		actualuser = db.GqlQuery("select * from User where user_id='"+username[1]+"'").fetch(1)
		user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		check_password = False
		if user.user_pw == hashlib.sha256(actual_password).hexdigest():
			check_password = True
		if not(username[0] or tel or len(date)==10 or not actualuser or check_password == True):
			if not username[0]:
				erroruser = 'Nombre invalido'
			if actualuser and actualuser[0].user_id != self.request.cookies.get('user_id').split("|")[0]:
					erroruser = 'Nombre ya existente'
			if not tel:
				errortel = 'Numero invalido'
			if not len(date)==10:
				errordate = 'Fecha invalida'
			if check_password == False:
				passerror = 'Contrasena erronea'
			self.render('editprofile.html',user=user[0],dateerror=errordate, erroruser=erroruser,errortel=errortel,date=user[0].user_date.split("-"),passerror=passerror)
		else:
			self.response.headers.add_header('Set-Cookie','user_id='+str(username[1])+'|'+str(user[0].user_pw)+';Path=/')
			user.user_id=username[1]
			user.user_tel=tel
			user.user_date=date
			user.user_desc=description
			user.put()
			time.sleep(2)
			self.redirect('/profile')
