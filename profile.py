import handler
import hashlib
import re
import time
from message import Message
from google.appengine.ext import db
from user import User

class Profile(handler.Handler):
	def get(self):
		user = self.request.cookies.get('user_id')
		messages = None
		if user:
			if user.split('|')[0].isdigit():
				if hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
					user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
				user_db = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user:
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
			if messages:
				messages = list(messages)
				for e in messages:
					e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
		if not self.request.get("u"):
			if not self.request.cookies.get("user_id"):
				self.redirect("/login")
			else:
				if user_db:
					self.render("profile.html",pagename='Perfil',user=user, user_ob=user_db,desc=user_db.user_desc,modificable=True,recent_msg=messages)
				else:
					self.redirect("/login")
		else:
			user_db = db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1)
			if user_db:
				if self.request.cookies.get("user_id"):
					if str(user_db[0].key().id()) == str(self.request.cookies.get("user_id").split("|")[0]):
						self.redirect("/profile")
					else:
						self.render("profile.html",pagename='Perfil',user=user, user_ob=user_db[0],desc=user_db[0].user_desc,recent_msg=messages)
				else:
					self.render("profile.html",pagename='Perfil',user=user, user_ob=user_db[0],desc=user_db[0].user_desc,recent_msg=messages)
			else:
				if self.request.get("u") == "ti":
					self.redirect("/profile")
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
		messages = None
		user = self.request.cookies.get('user_id')
		if user:
			if user.split('|')[0].isdigit():
				user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
			date_pre = create_date()
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
			if messages:
				messages = list(messages)
				for e in messages:
					e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
			self.render("editprofile.html",pagename='Editar Perfil', user=user,years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2],recent_msg=messages)
		else:
			self.write("Usuario no encontrado")
	def post(self):
		messages = None
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
		messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
		if messages:
			messages = list(messages)
			for e in messages:
				e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
		check_pass = False
		check_nick = True
		if hashlib.sha256(actual_password).hexdigest()==user.user_pw:
			check_pass = True
		if actualnick[0] != False:
			if actualnick[0][0].displayName != user.displayName:
				check_nick = False
		if (not nickname[0]) or (not tel[0]) or (len(date)<7) or (check_pass == False) or (check_nick == False):
			if not nickname[0]:
				erroruser = 'Nombre invalido'
			if not tel[0]:
				errortel = 'Numero invalido'
			if not len(date)>7:
				errordate = 'Fecha invalida'
			if check_pass ==False:
				passerror = 'Contrasena erronea'
			if check_nick == False:
				erroruser = 'Nombre tomado'
			date_pre = create_date()
			self.render('editprofile.html',pagename='Editar Perfil',user=user,dateerror=errordate, erroruser=erroruser,errortel=errortel,date=user.user_date.split("-"),
				years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2],passerror=passerror,recent_msg=messages)
		else:
			user.displayName=nickname[1]
			user.user_tel=tel[1]
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
		messages = None
		user = self.request.cookies.get('user_id')
		if user:
			user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
		if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
			if messages:
				messages = list(messages)
				for e in messages:
					e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
			self.render("editpass.html",pagename='Editar contrasenia', user=user,recent_msg=messages)
		else:
			self.write("Not found")
	def post(self):
		messages = None
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
		messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
		if messages:
			messages = list(messages)
			for e in messages:
				e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
		self.render('editpass.html',pagename='Editar contrasenia',user=user,errorpass=errorpass,errornew=errornew,errorverify=errorverify,recent_msg=messages)

class ViewPosts(handler.Handler):
	def get(self):
		messages = None
		if self.request.get("u"):
			user = self.request.cookies.get('user_id')
			if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
				user = user.split('|')[0]
				user = User.get_by_id(int(user))
				if not user:
					user = None
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
			if messages:
				messages = list(messages)
				for e in messages:
					e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
			profile = db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1)
			if len(profile) == 1:
				posts = db.GqlQuery("select * from Post where submitter='"+profile[0].user_id+"' order by created desc")
				posts = list(posts)
				if user:
					for e in posts:
						if e.submitter == user.user_id:
							e.submitter = "ti"
						else:
							e.submitter = self.request.get("u")+"|True"
				self.render('page.html',pagename='Ver posts',posts=posts,user=user)
			else:
				self.write("Perfil no encontrado")
		else:
			messages = None
			user = self.request.cookies.get('user_id')
			if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
				user = user.split('|')[0]
				user = User.get_by_id(int(user))
				if user:
					messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
					if messages:
						messages = list(messages)
						for e in messages:
							e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
					posts = db.GqlQuery("select * from Post where submitter='"+user+"' order by created desc")
					posts = list(posts)
					for e in posts:
						e.submitter = "ti"
					self.render('page.html',pagename='Ver posts',posts=posts,user=user,recent_msg=messages) 
				else:
					self.redirect("/login")

class ViewComments(handler.Handler):
	def get(self):
		user = self.request.cookies.get("user_id")
		messages = None
		if user and hashlib.sha256(user.split("|")[0]).hexdigest() == user.split("|")[1]:
			user = user.split("|")[0]
			user = User.get_by_id(int(user))
			if not user:
				self.redirect("/login")
		else:
			self.redirect("/login")
		messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
		if messages:
			messages = list(messages)
			for e in messages:
				e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
		if self.request.get("u"):
			profile = db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1)
			if len(profile) == 1:
				comments = db.GqlQuery("select * from Comment where submitter='"+profile[0].user_id+"' order by created desc")
				comments = list(comments)
				if user:
					for e in comments:
						if e.submitter == user.user_id:
							e.submitter = "ti"
						else:
							e.submitter = self.request.get("u")+"|True"
					if user.displayName == self.request.get("u"):
						self.render('just_comments.html',pagename='Ver comentarios',user=user,comments=comments, mios=True,recent_msg=messages)
					else:
						self.render('just_comments.html',pagename='Ver comentarios',user=user,comments=comments,author=self.request.get("u"))
				else:
					self.render('just_comments.html',pagename='Ver comentarios',user=user,comments=comments,author=self.request.get("u"),recent_msg=messages)	
			else:
				self.write("Perfil no encontrado")
		else:	
			comments = db.GqlQuery("select * from Comment where submitter='"+user.user_id+"' order by created desc")
			comments = list(comments)
			for e in comments:
				e.submitter = "ti"
			self.render("just_comments.html",pagename='Ver comentarios',user=user,comments=comments,mios=True,recent_msg=messages)

class SendPm(handler.Handler):
	def get(self):
		messages = None
		user = self.request.cookies.get("user_id")
		if user and user.split("|")[1] == hashlib.sha256(user.split("|")[0]).hexdigest() and User.get_by_id(int(user.split("|")[0])):
			user = User.get_by_id(int(user.split("|")[0]))
			if self.request.get("u"):
				destination = db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1)
				if len(destination) == 1:
					target = destination[0]
					if target.user_id == user.user_id:
						self.write("No puedes enviarte un mensaje a ti mismo")
					else:
						messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
						if messages:
							messages = list(messages)
							for e in messages:
								e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
						self.render("sendpm.html",user=user,target=target,pagename="Mensaje Privado",recent_msg=messages)
				else:
					self.write("Persona no encontrada")
			else:
				self.redirect("/")
		else:
			self.redirect('/login')
	def post(self):
		messages = None
		user = User.get_by_id(int(self.request.cookies.get("user_id").split("|")[0]))
		subject = self.request.get("pmtitle")
		if not subject:
			subject = "Sin asunto"
		content = self.request.get("pmcontent")
		destination = db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1)[0].user_id
		submitter = user.user_id
		if not content:
			messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"'")
			if messages:
				messages = list(messages)
				for e in messages:
					e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
			self.render("sendpm.html",user=user,target=destination,pagename="Mensaje Privado",error="Mensaje requerido",recent_msg=messages)
		else:
			msg = Message(submitter=submitter,destination=destination,subject=subject,content=content)
			msg.put()
			self.redirect("/profile?u="+self.request.get("u"))






