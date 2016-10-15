#clase para crear un post nuevo, depende del objeto Post

import handler
from post import Post
from user import User
import hashlib
import time

class Newpost(handler.Handler):
    def render_front(self,title = '',post = '',error = '',user=''):
        self.render('ascii.html',user=user,title=title,post=post,error=error,pagename='Postear')
    def get(self):
        user = self.request.cookies.get('user_id')
        if user:
            user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
        if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
            self.render_front(user=user)
        else:
            self.redirect('/signup')
    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')
        submitter = self.request.cookies.get('user_id').split('|')[0]
        submitter = User.get_by_id(int(submitter)).user_id
        if title and post:
            a = Post(title=title,post=post,submitter=submitter,modificable="False")
            a.created_str = str(a.created)
            a.created_str = a.created_str[0:16]
            a.put()           
            self.redirect('/'+str(a.key().id()))
        else:
            error = 'Titulo y contenido requeridos'
            user = self.request.cookies.get('user_id')
            if user:
                user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
            if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
                self.render_front(title,post,error,user)
            else:
                self.redirect('/signup')
            