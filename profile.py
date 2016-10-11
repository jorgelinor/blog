import handler
import hashlib
import re
import time
from google.appengine.ext import db
from user import User

class Profile(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		if user:
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

class EditProfile(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		if user:
			user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
			date_pre = create_date()
			self.render("editprofile.html", user=user,years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2])
		else:
			self.write("Not found")
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
			date_pre = create_date()
			self.render('editprofile.html',user=user[0],dateerror=errordate, erroruser=erroruser,errortel=errortel,
				date=user[0].user_date.split("-"),passerror=passerror,years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2])
		else:
			self.response.headers.add_header('Set-Cookie','user_id='+str(username[1])+'|'+str(user[0].user_pw)+';Path=/')
			user.user_id=username[1]
			user.user_tel=tel
			user.user_date=date
			user.user_desc=description
			user.put()
			time.sleep(2)
			self.redirect('/profile')


def create_date():
	years,months,days = [],[],[]
	for e in range(1,32):
		days.append(e)
	for e in range(1,13):
		months.append(e)
	for e in range(1950,2013):
		years.append(e)
	return (years,months,days)

class EditPass(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		if user:
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


