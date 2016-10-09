import newpost
from google.appengine.ext import db

class Page(newpost.Newpost):
    def get(self):
        user = self.request.cookies.get('user_id')
        if user:
        	user = user.split('|')[0]
        posts = db.GqlQuery('select * from Post')
        for e in posts:
            e.id_str = e.key().id()
        self.render('page.html',posts=posts,user=user) 
