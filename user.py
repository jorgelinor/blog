#Esta es la clase que sirve como objeto para el usuario y sus propiedades
from google.appengine.api import memcache
from google.appengine.ext import db
import logging


class User(db.Model):
	user_type = db.StringProperty(required=True)
	user_id = db.StringProperty(required=True)
	user_pw = db.StringProperty(required=True)
	user_mail = db.StringProperty(required=True)
	user_tel = db.StringProperty(required=True)
	user_date = db.StringProperty(required=True)
	user_desc = db.TextProperty(required=False)
	displayName = db.StringProperty(required=False)
	solicitud_cambio = db.BooleanProperty(required=False)
	rason_solicitud_cambio = db.TextProperty(required=False)
	banned_from_comments = db.BooleanProperty(required=False)
	banned_from_posting = db.BooleanProperty(required=False)
	state = db.BooleanProperty(required=False)
	img = db.StringProperty(required=False)

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid, parent = users_key())

	@classmethod
	def by_nickname(cls, name):
		u = User.all()
		for e in u:
			if e.displayName == name:
				return e
	@classmethod
	def by_username(cls, name):
		u = list(User.all())
		for user in u:
			if user.user_id == name:
				return user
		return None

# admin info para buscar los usuarios que solicitaron cambio de 
def user_cambio():
	reported = {}
	users= memcache.get("user_cache")
	
	for user in users:
		logging.error(users[user].state)
		if users[user].solicitud_cambio == True and users[user].state != True:
			reported[str(users[user].key().id())]=users[user]
	return reported


def user_cache():
	users ={}

	users_modificables =  db.GqlQuery("SELECT * FROM User ORDER by user_id")

	for p in users_modificables:
		users[str(p.key().id())] = p
	memcache.set("user_cache", users)