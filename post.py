#Esta es la clase que sirve como objeto para el post y sus propiedades
from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import handler

class Post(db.Model):
	topic = db.StringProperty(required=False)
	title = db.StringProperty(required=True)
	post = db.TextProperty(required=True)
	submitter = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
	created_str = db.StringProperty(required=False)
	modificable = db.StringProperty(required=True)
	razon = db.TextProperty(required=False)
	comments = db.IntegerProperty(required=True)
	visible = db.BooleanProperty(required=True)
	state = db.BooleanProperty(required=False)


	@classmethod
	def by_owner(self,name):
		result = []
		m = handler.Handler().get_data('Post','list')
		for post in m:
			if post.submitter == name:
				result.append(post)
		return result

	@classmethod
	def by_topic(cls,topic):
		result = []
		m = handler.Handler().get_data('Post','list')
		for post in m:
			if post.topic == topic:
				result.append(post)
		return result
# busca el post por topico
def buscar_topico(id_elemento, elemento):#id_elemento= topicos,Animales.etc: elemento= post_cache
	topic={}
	cache = memcache.get(elemento)
	# cantidad =  (cache[elemento].topic == id_elemento)
	for post in cache:
		if cache[post].topic == id_elemento:
			# logging.error(cache[post].topic)
			topic[str(cache[post].key().id())]=cache[post]
			logging.error(topic)
	return topic

# busca los post que se solicitan modificacion o permisos
def post_cambio():
	reported = {}
	posts = memcache.get("post_cache")

	for post in posts:
		if posts[post].modificable == 'pending' and posts[post].state == False:
			reported[str(posts[post].key().id())]=posts[post]
	return reported


# crea memcache de los post
def post_cache():
	post ={}
	post_modificables =  db.GqlQuery("SELECT * FROM Post ORDER BY created desc")
	for p in post_modificables:
		post[str(p.key().id())] = p
	memcache.set("post_cache", post)