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

PASS_RE = re.compile(r"^[a-zA-Z0-9]{3,20}$")
def valid_pass(password):
    if PASS_RE.match(password):
        return (True,password)
    return (False,password)

def valid_tel(tel):
	if not tel:
		return (False,tel)
	if tel.isdigit():
		if len(tel) > 7:
			return (True,tel)
	return (False,tel)

class EditProfile(handler.Handler):
	def get(self):
		user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
			self.render("editprofile.html", user=user,date=user.user_date.split("-"))
		else:
			self.write("Usuario no encontrado")
	def post(self):
		nickname = valid_username(self.request.get('nickname'))
		actual_password = self.request.get('actualpassword')
		tel = valid_tel(self.request.get('tel'))
		date = self.request.get('date1')+'-'+self.request.get('date2')+'-'+self.request.get('date3')
		description = self.request.get('description')
		erroruser,errortel,errordesc,errordate,passerror='','','','',''
		actualnick = [False]
		if db.GqlQuery("select * from User where displayName='"+nickname[1]+"'").fetch(1):
			actualnick[0] = db.GqlQuery("select * from User where displayName='"+nickname[1]+"'").fetch(1)
		user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		check_pass = False
		check_nick = True
		if hashlib.sha256(actual_password).hexdigest()==user.user_pw:
			check_pass = True
		if actualnick[0] != False:
			if actualnick[0][0].displayName != user.displayName:
				check_nick == False
		if (not nickname[0]) or (not tel[0]) or (len(date)!=10) or (check_pass == False) or (check_nick == False):
			if not nickname[0]:
				erroruser = 'Nombre invalido'
			if not tel[0]:
				errortel = 'Numero invalido'
			if not len(date)==10:
				errordate = 'Fecha invalida'
			if check_pass ==False:
				passerror = 'Contrasena erronea'
			if check_nick == False:
				erroruser = 'Nombre tomado'
			self.render('editprofile.html',user=user,dateerror=errordate, erroruser=erroruser,errortel=errortel,date=user.user_date.split("-"),passerror=passerror)
		else:
			user.displayName=nickname[1]
			user.user_tel=tel[1]
			user.user_date=date
			user.user_desc=description
			user.put()
			time.sleep(2)
			self.redirect('/profile')

class EditPass(handler.Handler):
	def get(self):
		user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
			self.render("editpass.html", user=user)
		else:
			self.write("Not found")
	def post(self):
		user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		oldpass = valid_pass(self.request.get('oldpass'))
		newpass = valid_pass(self.request.get('newpass'))
		verify = self.request.get('verify') == newpass[1]
		errorpass,errornew,errorverify = '','',''
		if oldpass[0]:
			if user.user_pw == hashlib.sha256(oldpass[1]).hexdigest():
				if newpass[0]:
					if verify:
						user.user_pw = hashlib.sha256(newpass[1]).hexdigest()
						user.put()
						time.sleep(2)
						self.redirect('/profile')
					else:
						errorverify = "Passwords doesn't match"
				else:
					errornew = 'Invalid password'
			else:
				errorpass = 'Incorrect password'
		else:
			errorpass = 'Invalid password'
		self.render('editpass.html',user=user,errorpass=errorpass,errornew=errornew,errorverify=errorverify)


