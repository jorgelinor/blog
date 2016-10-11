#esta es la clase que muestra los posts

import newpost
from user import User
import hashlib
from google.appengine.ext import db

class Page(newpost.Newpost):
    def get(self):
        user = self.request.cookies.get('user_id')
        if user and hashlib.sha256(user.split('|')[0]).hexdigest() == user.split('|')[1]:
        	user = user.split('|')[0]
        	user = User.get_by_id(int(user)).user_id
        else:
        	user = None
        posts = db.GqlQuery('select * from Post')
        for e in posts:
            e.id_str = e.key().id()
        self.render('page.html',posts=posts,user=user) 
