#esta es la clase que muestra los posts
import newpost
from user import User
import hashlib
from google.appengine.ext import db
from google.appengine.api import memcache
from handler import Handler


class Page(newpost.Newpost):
    def get(self):
    	posts = self.get_data('posts',db.GqlQuery('select * from Post order by created desc'))
        self.load_data(lim=5,pagename="Pagina Principal",posts=posts)
