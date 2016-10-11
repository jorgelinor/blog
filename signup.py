#Clase de registro

import handler
from user import User
import hashlib
import re
from google.appengine.ext import db

class Signup(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		if not user:
			self.render('signup.html',url='Signup',link='/')
		else:
			self.write("<a href='/'>Already registered</a>")
	def post(self):
		username = valid_username(self.request.get('username'))
		password = valid_pass(self.request.get('password'))
		tel = self.request.get('tel')
		date = self.request.get('date1')+'-'+self.request.get('date2')+'-'+self.request.get('date3')
		description = self.request.get('description')
		verify = self.request.get('verify')==self.request.get('password')
		email = valid_email(self.request.get('email'))
		erroruser,errormail,errorpass,errorverify,errortel,errordesc,errordate='','','','','','',''
		user_query = db.GqlQuery('select * from User')
		user_list = []
		user_ob = None #<---esta variable la uso mucho a la hora de asignar un objeto usuario
		if user_query:
			for e in user_query:
				user_list.append(e.user_id)
				if e.user_id == username[1]:
					user_ob = e
		if not(username[0] and tel and len(date)==10 and email and password[0] and verify and email[0] and not user_ob):
			if not username[0]:
				erroruser = 'Invalid username'
			if user_ob:
				erroruser = 'Username already exists'
			if not password[0]:
				errorpass = 'Invalid password'
			if not verify:
				errorverify = "Passwords don't match"
			if not tel:
				errortel = 'Introduce a phone number'
			if not len(date)==10:
				errordate = 'Introduce a Birth Date'
			if not email[0]:
				errormail = 'Invalid e-mail'
			self.render('signup.html',username=username[1],email=email[1],erroruser=erroruser,errormail=errormail,errorpass=errorpass,errorverify=errorverify,
						errortel=errortel,errordate=errordate,errordesc=errordesc,tel=tel,description=description,date=date)
		else: #si el registro es valido
			user_ob = User(user_id=username[1],user_pw=hashlib.sha256(password[1]).hexdigest(),user_mail=email[1],
							user_tel=tel,user_date=date,user_desc=description,user_type='user') #se crea un objeto usuario con los datos
			user_ob.put() #se sube a la base de datos
			self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.user_id)+'|'+str(user_ob.user_pw)+';Path=/') #y se crea la cookie
			self.redirect('/')


#estas funciones sirven para validar el usuario,la contrasenia y el email, pero se le pueden agregar mas condiciones al verificar.
#Las salidas de dichas funciones son una tupla con un boolean como primer elemento y el usuario,contrasenia o email en el segundo
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

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    if email== "":
        return None
    if EMAIL_RE.match(email):
        return (True,email)
    return (False,email)