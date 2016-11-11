#Esta es la clase que sirve como objeto para el usuario y sus propiedades

from google.appengine.ext import db

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
	def by_name(cls, name):
		u = User.all().filter('displayName =', name).get()
		return u

	def user_cache():
		users ={}

		users_modificables =  db.GqlQuery("SELECT * FROM User ORDER by user_id")

		for p in users_modificables:
			users[str(p.key().id())] = p
		memcache.set("user_permisos_cache", users)
		return users