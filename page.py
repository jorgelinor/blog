#esta es la clase que muestra los posts
import newpost
from user import User
from post import *
import hashlib
from google.appengine.ext import db
from google.appengine.api import memcache
from handler import Handler


class Page(newpost.Newpost):
    def get(self):
    	posts = self.get_data('Post','list')
        self.load_data(lim=5,pagename="Pagina Principal",posts=posts)
