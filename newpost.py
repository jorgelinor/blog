#clase para crear un post nuevo, depende del objeto Post

import handler
from post import Post
from user import User
import hashlib
import time
from google.appengine.ext import db
from google.appengine.api import memcache

class Newpost(handler.Handler):
    def render_front(self,title = '',post = '',errorS = '',errorT='',errorC='',user='',recent_msg=None):
        self.render('ascii.html',user=user,title=title,post=post,errorS = '',errorT='',errorC='',pagename='Postear',recent_msg=recent_msg)
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)
            if not user.banned_from_posting:
                self.render_front(user=user,recent_msg=messages)
            else:
                self.redirect('/')
        else:
            self.redirect('/signup')
    
    def post(self,errorS='',errorC='',errorT=''):
        topic = self.request.get('topic')
        title = self.request.get('subject')
        post = self.request.get('content')
        submitter = self.get_cookie_user(self.request.cookies.get('user_id'))[1]
        messages = self.GetMessages(actualizar=False,persona=submitter)
        if title and post and topic:

            a = Post(topic= topic, title=title,post=post,submitter=submitter.user_id,modificable="False",comments=0,visible=True,state=False,likes=0,dislikes=0)

            a.created_str = str(a.created)
            a.created_str = a.created_str[0:16]
            self.get_data('posts',db.GqlQuery('select * from Post order by created desc'),actualizar=True)
            a.put()           
            self.redirect('/'+str(a.key().id()))
            memcache.delete('cantidad_'+self.request.get("topic"))
        else:
            if len(title)<1:
                errorS = 'Titulo requerido'
            if len(post)<1:
                errorC = 'Contenido de post requerido'
            if len(topic)<1:
                errorT = 'Topico de post requerido'
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            self.render_front(title,post,errorS,errorC,errorT,user,messages)
        else:
            self.redirect('/signup')
            
