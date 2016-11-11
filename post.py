#Esta es la clase que sirve como objeto para el post y sus propiedades
from google.appengine.ext import db

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

	def submitter_user(nombre):
		post = Post.all().filter('submitter =', nombre).get()
		return post

	def buscar_topico(id_elemento, elemento):
	    cache = memcache.get(elemento)
	    cantidad =  (cache[elemento].values().topic == id_elemento)
	    if id_elemento in cache:
	        return cache[id_elemento]

	def post_cache():
		post ={}
		post_modificables =  db.GqlQuery("SELECT * FROM Post ORDER BY created desc")
		for p in post_modificables:
			post[str(p.key().id())] = p
		memcache.set("post_cache", post)
		return post