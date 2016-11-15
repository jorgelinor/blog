from google.appengine.ext import db
from google.appengine.api import memcache

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



def user_comment(nombre):
	comment = Comment.all().filter('submitter =', nombre).get()
	return comment

def comment_repost():
	reported= Comment.all().filter('reported =', True).get()

def busqueda_comment(nombre):
	listas={}
	comments = memcache.get("comments_cache")
	if comment is None:
		cache=comments_cache()
		comments = cache["comments_cache"]
	for comment in comments:
		if nombre in comment.submitter:
			listas[str(comment.key().id())]= comment
	return listas

def comments_cache():
    # comentario cre el cache para el content de comments
    comments = {}
    banned_comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created desc")
    for p in banned_comments:
    	comments[str(p.key().id())] = p
    	memcache.set("comments_cache", comments)
    	# logging.error(comments)
    return comments