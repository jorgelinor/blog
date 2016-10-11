#Clase de inicio de sesion

import handler
import hashlib
from user import User
import re
from google.appengine.ext import db

class Login(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		if user:
			user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
			self.write("<a href='/'>Already logged</a>")
		else:
			self.render('login.html',url='Login',link='/')
	def post(self):
		username = valid_username(self.request.get('username'))
		password = valid_pass(self.request.get('password'))
		erroruser,errorpass='',''
		user_query = db.GqlQuery('select * from User where user_id=:1',username[1])
		user_query = list(user_query)
		user_ob = None #<---esta variable la uso mucho a la hora de asignar un objeto usuario
		if user_query:
			user_ob = user_query[0]
		if not(username[0] and password[0] and user_ob and user_ob.user_pw == hashlib.sha256(password[1]).hexdigest()):
			if not username[0]:
				erroruser = 'Invalid username'
			if not user_ob:
				erroruser = "Username doesn't exist"
			if not password[0]:
				errorpass = 'Invalid password'
			if user_ob and user_ob.user_pw != hashlib.sha256(password[1]).hexdigest():
				errorpass = 'Invalid password'
			self.render('login.html',username=username[1],erroruser=erroruser,errorpass=errorpass)
		else: #si todo esta correcto
			self.write(str(user_ob.key().id()))
			self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.key().id())+'|'+hashlib.sha256(str(user_ob.key().id())).hexdigest()+';Path=/') #se hace la cookie del usuario
			self.redirect('/profile')

#estas funciones sirven para validar el usuario y la contrasenia, pero se le pueden agregar mas condiciones al verificar.
#Las salidas de dichas funciones son una tupla con un boolean como primer elemento y el usuario o contrasenia en el segundo
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
