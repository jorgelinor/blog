import handler
from post import Post

class Newpost(handler.Handler):
    def render_front(self,title = '',post = '',error = ''):
        self.render('ascii.html',title=title,post=post,error=error)
    def get(self):
        username = self.request.cookies.get('user_id')
        if username:
            self.render_front()
        else:
            self.redirect('/signup')
    def post(self):
        title = self.request.get('subject')
        post = self.request.get('content')
        submitter = self.request.cookies.get('user_id')
        if title and post:
            a = Post(title=title,post=post,submitter=submitter.split('|')[0])
            a.created_str = str(a.created)
            a.created_str = a.created_str[0:16]
            a.put()            
            self.redirect('/')
        else:
            error = 'we need more...'
            self.render_front(title,post,error)