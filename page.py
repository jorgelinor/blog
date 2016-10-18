#esta es la clase que muestra los posts

import newpost
from user import User
import hashlib
from google.appengine.ext import db
from google.appengine.api import memcache
from handler import Handler


class Page(newpost.Newpost):
    def get(self):
        user = None
        messages = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_id',self.get_cookie_user(self.request.cookies.get('user_id'))[1])
        posts = self.get_data('posts',db.GqlQuery('select * from Post order by created desc'))
        posts = list(posts)
        for e in posts:
            if user != None and e.submitter == user.user_id:
                e.submitter = "ti"
            else:
                submitter = self.get_data('submitter',db.GqlQuery("select * from User where user_id='"+e.submitter+"'"))
                submitter = list(submitter)
                if len(submitter) < 1:
                    e.submitter = e.submitter+"|False"
                else:
                    e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName+"|True"
        if user != None:
            messages = db.GqlQuery("select * from Message where destination='"+user.user_id+"' order by date desc")
            if messages:
                messages = list(messages)
                for e in messages:
                    if e.submitter != "Administracion":
                        e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName          
        self.render('page.html',pagename='Pagina principal',posts=posts,user=user,recent_msg=messages) 
