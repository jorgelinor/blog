#Esta es la clase que sirve como objeto para el post y sus propiedades
from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty(required=True)
    post = db.TextProperty(required=True)
    submitter = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    created_str = db.StringProperty(required=False)
    modificable = db.StringProperty(required=True)
    razon = db.TextProperty(required=False)
