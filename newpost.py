#clase para crear un post nuevo, depende del objeto Post

import handler
from post import Post
from user import User
import hashlib
import time
from google.appengine.ext import db

class Newpost(handler.Handler):
    def render_front(self,title = '',post = '',error = '',user='',recent_msg=None):
        self.render('ascii.html',user=user,title=title,post=post,error=error,pagename='Postear',recent_msg=recent_msg)
    def get(self):
        messages = None
        user = self.request.cookies.get('user_id')
        if user:
            user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
        messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
        if messages:
            messages = list(messages)
            for e in messages:
                if e.submitter != "Administracion":
                    e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
        if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
            messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
            if messages:
                messages = list(messages)
                for e in messages:
                    if e.submitter != "Administracion":
                        e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
            if not user.banned_from_posting:
                self.render_front(user=user,recent_msg=messages)
            else:
                self.redirect('/')
        else:
            self.redirect('/signup')
    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')
        submitter = self.request.cookies.get('user_id').split('|')[0]
        submitter = User.get_by_id(int(submitter)).user_id
        messages = db.GqlQuery("select * from Message where destination='"+submitter+"'")
        if messages:
            messages = list(messages)
            for e in messages:
                if e.submitter != "Administracion":
                    e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
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
                self.render_front(title,post,error,user,messages)
            else:
                self.redirect('/signup')
            