from google.appengine.ext import db
from google.appengine.api import memcache
from post import *
from comment import *
import logging


class LikesDislike(db.Model):
	id_objeto = db.IntegerProperty(required=True)
	id_person = db.IntegerProperty(required=True)
	like = db.BooleanProperty(required=False)
	dislike = db.BooleanProperty(required=False)

def verificaruser(id_user, id_object, desicion):
	cacheL = memcache.get('likesdilike_cache')
	cacheP = memcache.get('post_cache')
	cacheC = memcache.get('comments_cache')
	logging.error(id_user+"**"+id_object+"**"+desicion)
	if cacheL is None:
		comments_cache()
		post_cache()
		likes_cache()
	if desicion == 'likes':
		if cacheL[id_person]:
			objeto = cacheL[id_person]
			if objeto.dislike == True :
				objeto.like = True
				objeto.dislike= False
				objeto.put()
				if cacheP[id_object]:
					cacheP[id_object].like+=1
					cacheP[id_object].dislike+=1
					cacheP[id_object].put()
				elif cacheC[id_object]:
					cacheC[id_object].like+=1
					cacheC[id_object].dislike+=1
					cacheC[id_object].put()
			return True
		else:	
			like = LikesDislike(id_objeto=id_object,id_person=int(id_user),like=True,dislike=False)
			like.put()
			if cacheP[id_object]:
				cacheP[id_object].like+=1
				cacheP[id_object].dislike+=1
				cacheP[id_object].put()
			elif cacheC[id_object]:
				acheC[id_object].like+=1
				cacheC[id_object].dislike+=1
				cacheC[id_object].put()
			return False

	elif desicion == 'dislike':
		if cacheL[id_person]:
			objeto = cacheL[id_person]
			if objeto.dislike == True :
				objeto.like = True
				objeto.dislike= False
				objeto.put()
				if cacheP[id_object]:
					cacheP[id_object].like+=1
					cacheP[id_object].dislike-=1
					cacheP[id_object].put()
				elif cacheC[id_object]:
					cacheC[id_object].like+=1
					cacheC[id_object].dislike-=1
					cacheC[id_object].put()
		return True
	else:	
		like = LikesDislike(id_objeto=id_object,id_person=id_user,like=True,dislike=False)
		like.put()
		if cacheP[id_object]:
			cacheP[id_object].like-=1
			cacheP[id_object].dislike+=1
			cacheP[id_object].put()
		elif cacheC[id_object]:
			acheC[id_object].like-=1
			cacheC[id_object].dislike+=1
			cacheC[id_object].put()
		return False



def likes_cache():
	LikesDislike= {}
	likes = db.GqlQuery("SELECT * FROM LikesDislike ORDER BY desc")
	for p in likes:
		LikesDislike[str(p.id_person)] = p
		memcache.set("likesdilike_cache", comments)

