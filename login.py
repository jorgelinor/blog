#Clase de inicio de sesion

import handler
import hashlib
from user import User
import re
from google.appengine.ext import db

class Login(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		if not user:
			self.render('login.html',url='Login',link='/')
		else:
			self.write("<a href='/'>Already logged</a>")
	def post(self):
		username = valid_username(self.request.get('username'))
		password = valid_pass(self.request.get('password'))
		erroruser,errorpass='',''
		user_query = db.GqlQuery('select * from User')
		user_list = []
		user_ob = None #<---esta variable la uso mucho a la hora de asignar un objeto usuario
		if user_query:
			for e in user_query:
				user_list.append(e.user_id)
				if e.user_id == username[1]:
					user_ob = e
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
			self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.user_id)+'|'+str(user_ob.user_pw)+';Path=/') #se hace la cookie del usuario
			self.redirect('/')

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