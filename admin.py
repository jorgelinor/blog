from google.appengine.ext import db
from google.appengine.api import memcache
import handler
import hashlib
from user import User
from post import Post
import time
from message import Message
from comment import Comment

class Admin(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == "admin":
                messages = self.GetMessages(actualizar=False,persona=user)
                self.render("admin.html", pagename="Administracion",user=user,recent_msg=messages)
            else:
                self.redirect("/")
        else:
            self.redirect("/login")

class PostRequest(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == "admin":
                posts = self.get_data("pending_posts",db.GqlQuery("select * from Post where modificable='pending'"))
                if self.request.get("post"):
                    post = Post.get_by_id(int(self.request.get("post")))
                    if post:
                        if self.request.get("action") == "accept_request":
                            post.modificable = 'True'
                            self.delete_data('post_'+str(post.key().id()))
                            message = Message(submitter="Administracion", destination=post.submitter, subject="<div style='color:green'><b>PEDIDO ACEPTADO</b></div>", content="Se ha aceptado su pedido para cambiar <a href='/"+self.request.get("post")+"'>este post.</a>")
                            message.put()
                            post.put()
                            self.redirect("/admin/post_requests")
                        elif self.request.get("action") == "deny_request":
                            post.modificable = "False"
                            self.delete_data('post_'+str(post.key().id()))
                            message = Message(submitter="Administracion", destination=post.submitter, subject="<div style='color:red'><b>PEDIDO DENEGADO</b></div>", content="Se ha denegado su pedido para cambiar <a href='/"+self.request.get("post")+"'>este post.</a>")
                            message.put()
                            post.put()
                            self.redirect("/admin/post_requests")
                        else:
                            self.redirect("/admin/post_requests")
                    else:
                        self.redirect("/admin/post_requests")
                elif posts:
                    messages = self.GetMessages(actualizar=False,persona=user)
                    self.render("page.html", user=user,posts=posts,pagename="Edicion de publicaciones",recent_msg=messages,request=True)
                else:
                    self.write("No hay posts pendientes por el momento")
            else:
                self.redirect("/")
        else:
            self.redirect("/login")


class Users(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == "admin":
                users = self.get_data("users_admin",db.GqlQuery("select * from User"))
                profile = self.get_data(self.request.get("u"),db.GqlQuery("select * from User where user_id='"+self.request.get("u")+"'"))
                if len(list(profile))>0:
                    profile = list(profile)[0]
                    changed = False
                    if self.request.get("action"):
                        if self.request.get("action") == "ascend":
                            profile.user_type = "admin"
                            changed = True
                        if self.request.get("action") == "descend":
                            profile.user_type = "user"
                            changed = True
                        if self.request.get("action") == "ban_posting":
                            profile.banned_from_posting = True
                            changed = True
                        if self.request.get("action") == "allow_posting":
                            profile.banned_from_posting = False
                            changed = True
                        if self.request.get("action") == "ban_comments":
                            profile.banned_from_comments = True
                            changed = True
                        if self.request.get("action") == "allow_comments":
                            profile.banned_from_comments = False
                            changed = True
                        if changed == True:
                            profile.put()
                        self.redirect("/admin/users")
                    else:
                        self.redirect("/admin/users")
                else:
                    messages = self.GetMessages(actualizar=False,persona=user)
                    self.render("users.html",users=users,pagename="Panel de usuarios", user=user,recent_msg=messages)
            else:
                self.redirect("/")
        else:
            self.redirect("/login")

class Reports(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == "admin":
                messages = self.GetMessages(actualizar=False,persona=user)
                reported_comments = self.get_data("reported_comments",db.GqlQuery('select * from Comment where reported=True'))
                self.render('reported.html',user=user,pagename='Reportes',comments=list(reported_comments),recent_msg=messages)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')


class DeleteComment(handler.Handler):
    def get(self,link):
        comment = Comment.get_by_id(int(link))
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == 'admin':
                post = Post.get_by_id(int(comment.post))
                post.comments -= 1
                post.put()
                self.delete_data('post_'+str(post.key().id()))
                db.delete(comment)
                time.sleep(2)
                self.redirect('/admin/reports')
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

class KeepComment(handler.Handler):
    def get(self,link):
        comment = Comment.get_by_id(int(link))
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == 'admin':
                comment.razon = []
                comment.reported = False
                comment.put()
                time.sleep(2)
                self.redirect('/admin/reports')
            else:
                self.redirect('/')
        else:
            self.redirect('/login')
