from google.appengine.ext import db
from google.appengine.api import memcache
import handler
import hashlib
from user import User
from post import Post
import time
from message import Message
from comment import Comment
import logging
import json

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
# fabian
# 
# 
class Admin_info(handler.Handler):
    def get(self):
        logging.error('entro')
        # los querys deben ser comments_reported_cache o 
        # post_modificable_cache o user_permisos_cache o post_reposrted_cache
        action = self.request.GET.get('action')

        info = memcache.get(action)
        if info is None:
            createquerty(action)
            info = memcache.get(action)
        informacion = diccionarisarcache(info,action)
        logging.error(action,info)
        self.write(json.dumps(informacion))
    def post(self, query):
        if query == 'comments_reported_cache':
            pass
        elif query == 'post_modificable_cache':
            pass
        elif query == 'user_permisos_cache':
            pass
        elif query == 'post_reposrted_cache':
            pass
# clase de admind para manejar los reportes de los comentario reportados para determinar si son validos de mostar o no 
# muestra los post de los cuales los creadores desean modifcar o actualizar con informacion
# les cambia el atributo al post para ser modificado solo por el creador 
#permite el a un usuario cambiar su capacidad de manejo en la pagina como admin o revocar permisos de usuarios
# de terminar si u post reportado tiene un contenido que se puede mostrar


# convierte el objeto de la base de datos a una diccionario lejible para json  
def diccionarisarcache(info,cual):
    #info es la cache creada solo con la informacion de echa
    if cual == 'comments_reported_cache':
        for partes in info:
                informacion={info[partes].submitter:{'title':info[partes].title,
                                                      'content':info[partes].content,
                                                      'post':info[partes].post,
                                                      'submitter':info[partes].submitter,
                                                      'created':info[partes].created.strftime('%y/%m/%d'),
                                                      'created_str':info[partes].created_str,
                                                      'reported':info[partes].reported,
                                                      'razon':info[partes].razon
                                                    }
                            }
    elif cual == 'post_modificable_cache':
        for partes in info:
                informacion={info[partes].submitter:{'topic':info[partes].topic,
                                                      'title':info[partes].title,
                                                      'content':info[partes].content,
                                                      'post':info[partes].post,
                                                      'submitter':info[partes].submitter,
                                                      'created':info[partes].created.strftime('%y/%m/%d'),
                                                      'created_str':info[partes].created_str,
                                                      'modificable':info[partes].modificable,
                                                      'razon':info[partes].razon
                                                    }}
    elif cual == 'user_permisos_cache':
        for partes in info:
                informacion={info[partes].displayName:{"user_type":info[partes].user_type,
                                            "user_id":info[partes].user_type,
                                            "displayName":info[partes].displayName,
                                            "solicitud_cambio":info[partes].solicitud_cambio,
                                            "rason_solicitud_cambio":info[partes].rason_solicitud_cambio,
                                            "banned_from_comments":info[partes].banned_from_comments,
                                            "banned_from_posting":info[partes].banned_from_posting
                                                    }}
    return informacion                    
# crea el query deacuerdo ala info pedidad por el admin
def createquerty(content):
    if content == "comments_reported_cache":# comentario reportados
        comments = {}
        banned_comments = db.GqlQuery("SELECT * FROM Comment WHERE reported = True ORDER BY created desc")
        for p in banned_comments:
            comments[p.title] = p
        memcache.set("comments_reported_cache", comments)
        logging.error(comments)
        return comments
    elif content == 'post_modificable_cache':#solicitud de modiicar un post post
        post ={}
        post_modificables =  db.GqlQuery("SELECT * FROM Post WHERE  Post.modificable = 'pending' ORDER BY created desc")
        for p in post_modificables:
            post[p.title] = p
        memcache.set("post_modificable_cache", post)
        return post
    elif content == 'user_permisos_cache':# permisos para usuarios
        users ={}
        users_modificables =  db.GqlQuery("SELECT * FROM User WHERE User.solicitud_cambio = True ORDER BY created desc")
        for p in post_modificables:
            users[p.subject] = p
        memcache.set("user_permisos_cache", users)
        return users
    elif content == 'post_reposrted_cache':#post reportados
        post_repo ={}
        post_reported =  db.GqlQuery("SELECT * FROM Post WHERE Post.repost = True ORDER BY created desc")
        for p in post_reported:
            post_repo[p.subject] = p
        memcache.set("post_reposrted_cache", post)
        return post_repo


# Form_html="""
#     {% for content in action %}
#     <form>
        # <h1>coment submete by: {{action[content].submitter}}</h1>
        # <b> crado: {{action[content].created_str}}</b>
        # <br>
        # <h4>post <a href="{{action[content].post}}">Post del mensaje</a></h4>
        # <div>
        #     {{action[content].content}}
        # </div>
        # <h3>Reportado</h3><br>
        # <b>{{action[content].razon}}</b>
#     </form>
#     <br>
#     {% endfor %}
# """