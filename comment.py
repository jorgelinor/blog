from google.appengine.ext import db
from google.appengine.api import memcache
import logging
from handler import *

class Comment(db.Model):
	title = db.TextProperty(required=True)
	content = db.TextProperty(required=True)
	post = db.StringProperty(required=True)
	submitter = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	created_str = db.StringProperty(required=False)
	reported = db.BooleanProperty(required=True)
	razon = db.ListProperty(str,required=True)
	state= db.BooleanProperty(required=False)



# def user_comment(nombre):
# 	comment = Comment.all().filter('submitter =', nombre).get()
# 		return comment


# busca el comentario por el usuario que lo somtio
	@classmethod
	def busqueda_comment(cls,nombre):
		listas=[]
		comments = Handler().get_data('Comment','list')
		for comment in comments:
			if nombre == comment.submitter:
				listas.append(comment)
		return listas

	@classmethod
	def by_post(cls,post):
		listas=[]
		comments = Handler().get_data('Comment','list')
		for comment in comments:
			if post == comment.post:
				listas.append(comment)
		return listas


#retorna comentarios reportados 
def comment_report():
	reported= {}
	comments = memcache.get("comments_cache")

	for comment in comments:
		if comments[comment].reported == True and comments[comment].state == False:
			reported[str(comments[comment].key().id())]=comments[comment]
	return reported


# crea ql query para el memcache
def comments_cache():
    # comentario cre el cache para el content de comments
    comments = {}
    banned_comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created desc")
    for p in banned_comments:
    	comments[str(p.key().id())] = p
    	memcache.set("comments_cache", comments)
    	# logging.error(comments)