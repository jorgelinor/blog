from google.appengine.ext import db
from google.appengine.api import memcache
import handler

class Message(db.Model):
	submitter = db.StringProperty(required=True)
	destination = db.StringProperty(required=True)
	subject = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True)

	@classmethod
	def by_destination(self,name):
		m = handler.Handler().get_data('Message','list')
		return m
	@classmethod
	def update(self,destination,msg):
		mensajes = memcache.get('Message')
		mensaje = mensajes.get(destination)
		if mensaje:
			mensaje.insert(0,msg)
		else:
			mensaje = list(db.GqlQuery("select * from Message where destination='%s'"%destination))
			mensajes[destination] = mensaje
		memcache.set('Message',mensajes)