#esta es la clase que muestra los posts

import newpost
from user import User
import hashlib
from google.appengine.ext import db
from google.appengine.api import memcache
from handler import Handler


class Page(newpost.Newpost):
    def get(self,messages=None):
        posts = self.get_data('posts',db.GqlQuery('select * from Post order by created desc'))
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)
        posts = self.display_names(user,list(posts))
        self.render('page.html',pagename='Pagina principal',posts=posts,user=user,recent_msg=messages) 
