#clase para crear un post nuevo, depende del objeto Post

import handler
from post import Post
from user import User
import hashlib

class Newpost(handler.Handler):
    def render_front(self,title = '',post = '',error = ''):
        self.render('ascii.html',title=title,post=post,error=error)
    def get(self):
        user = self.request.cookies.get('user_id')
        if user:
            user = User.get_by_id(int(self.request.cookies.get('user_id').split('|')[0]))
        if user and hashlib.sha256(self.request.cookies.get('user_id').split('|')[0]).hexdigest() == self.request.cookies.get('user_id').split('|')[1]:
            self.render_front()
        else:
            self.redirect('/signup')
    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')
        submitter = self.request.cookies.get('user_id').split('|')[0]
        submitter = User.get_by_id(int(submitter)).user_id
        if title and post:
            a = Post(title=title,post=post,submitter=submitter)
            a.created_str = str(a.created)
            a.created_str = a.created_str[0:16]
            a.put()            
            self.redirect('/')
        else:
            error = 'we need more...'
            self.render_front(title,post,error)