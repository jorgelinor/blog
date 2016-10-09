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
		user_ob = None
		if user_query:
			for e in user_query:
				user_list.append(e.user_id)
				if e.user_id == username[1]:
					user_ob = e
		if not(username[0] and password[0] and user_ob and user_ob.user_pw == hashlib.sha256(username[1]+password[1]).hexdigest()):
			if not username[0]:
				erroruser = 'Invalid username'
			if not user_ob:
				erroruser = "Username don't exists"
			if not password[0]:
				errorpass = 'Invalid password'
			if user_ob and user_ob.user_pw != hashlib.sha256(password[1]).hexdigest():
				errorpass = 'Invalid password'
			self.render('login.html',username=username[1],erroruser=erroruser,errorpass=errorpass)
		else:
			user_ob = User(user_id=username[1],user_pw=hashlib.sha256(username[1]+password[1]).hexdigest())
			self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.user_id)+'|'+str(user_ob.user_id+user_ob.user_pw)+';Path=/')
			self.redirect('/')


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