#esta es la clase que muestra los posts
# -*- coding: utf-8 -*-
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
        self.load_data(lim=5,pagename=u"Página Principal",posts=posts)

class FilterPosts(Handler):
	"""docstring for ClassName"""
	def get(self, link):
		if link:
			if link.title() == 'News':
				posts = self.get_data('Post','list')
				self.load_data(lim=5,pagename=u"Página Principal",posts=posts)
			else:
				try:
					posts = Post.by_topic(link.title())
					self.load_data(lim=5,pagename=u"Página Principal",posts=posts)
				except self.redirect('/') as e:
					raise e
		