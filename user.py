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
