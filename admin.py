from google.appengine.ext import db
from google.appengine.api import memcache
import handler
import hashlib
from user import *
from post import *
from comment import *
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
            messages = self.GetMessages(actualizar=False,persona=user)
            if user.user_type == "admin":
                posts = self.get_data("pending_posts",list(db.GqlQuery("select * from Post where modificable='pending'")))
                if self.request.get("post"):
                    post = Post.get_by_id(int(self.request.get("post")))
                    if post:
                        if self.request.get("action") == "accept_request":
                            post.modificable = 'True'
                            self.get_data('post_'+str(post.key().id()),post,actualizar=True)
                            message = Message(submitter="Administracion", destination=post.submitter, subject="<div style='color:green'><b>PEDIDO ACEPTADO</b></div>", content="Se ha aceptado su pedido para cambiar <a href='/"+self.request.get("post")+"'>este post.</a>")
                            message.put()
                            post.put()
                            self.redirect("/admin/post_requests")
                        elif self.request.get("action") == "deny_request":
                            post.modificable = "False"
                            self.get_data('post_'+str(post.key().id()),post,actualizar=True)
                            message = Message(submitter="Administracion", destination=post.submitter, subject="<div style='color:red'><b>PEDIDO DENEGADO</b></div>", content="Se ha denegado su pedido para cambiar <a href='/"+self.request.get("post")+"'>este post.</a>")
                            message.put()
                            post.put()
                            self.redirect("/admin/post_requests")
                        else:
                            self.redirect("/admin/post_requests")
                    else:
                        self.redirect("/admin/post_requests")
                elif len(posts)<1:
                    posts = None
            else:
                self.redirect("/")
        else:
            self.redirect("/login")
        self.render("page.html", user=user,posts=posts,pagename="Edicion de publicaciones",recent_msg=messages,request=True)

# fabian
# 
# 
class Admin_info(handler.Handler):
    def get(self):
        # los querys deben ser comments_reported_cache o 
        # post_modificable_cache o user_permisos_cache o post_reposrted_cache
        # if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])

            if user.user_type == "admin":
                info={}
                action = self.request.GET.get('action')
                informacion= memcache.get(action)
                if informacion is None:
                    post_cache()
                    user_cache()
                    comments_cache()
                    
                if action == 'comments_cache':
                    info = comment_report()

                elif action =='user_cache':
                    info = user_cambio()

                elif action =='post_cache':
                    info = post_cambio()
    
                informacion = diccionarisarcache(info,action)
                self.write(json.dumps(informacion))
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

class Users(handler.Handler):
    def get(self):
        logging.error('nooooooooooooooooooooo')
        user = self.request.GET.get('user')
        topicos = buscar_user_tipe(user)
        informacion = diccionarisarcache(topicos,'user_cache')
        self.write(json.dumps(informacion))


class Topicos(handler.Handler):
    def get(self):
        topi= self.request.GET.get('topico')
        topicos = buscar_topico("post_cache",topi)
        informacion = diccionarisarcache(topicos,'post_cache')
        self.write(json.dumps(informacion))
        

        

# clase de admind para manejar los reportes de los comentario reportados para determinar si son validos de mostar o no 
# muestra los post de los cuales los creadores desean modifcar o actualizar con informacion
# les cambia el atributo al post para ser modificado solo por el creador 
#permite el a un usuario cambiar su capacidad de manejo en la pagina como admin o revocar permisos de usuarios
# de terminar si u post reportado tiene un contenido que se puede mostrar


class Admin_submit(handler.Handler):
    def get(self, id_obj):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            if user.user_type == "admin":
                query=''
                ins, id_object = id_obj.split('_')[0], id_obj.split('_')[1]
                if ins == 'come':
                    query='comments_cache'
                elif ins == 'post':
                    query='post_cache'
                elif ins == 'user':
                    query='user_cache'

                info = buscar(id_object , query)
                self.render('upload.html',info=info, query=query,user=user)
            else:
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, id_obj):
        ins, id_object = id_obj.split('_')[0], id_obj.split('_')[1]
        if ins == 'come':
            # coment_id = self.request.get('comment_id')
            comments_reported = self.request.get('report')

            cache = buscar(id_object, 'comments_cache')
            if cache and comments_reported == 'on':
                cache.show = False
                cache.state = True
                cache.put()
                self.redirect('/admin')
            else:
                cache.show = True
                cache.state = True
                cache.put()
                self.redirect('/admin')

        elif ins == 'post':
            modificable = self.request.get('permiso')
            cache = buscar(id_object, 'post_cache')
            if cache and modificable:
                cache.modificable = modificable
                cache.state = True
                cache.put()
                self.redirect('/admin')
            else:
                self.redirect('/admin')
        elif ins == 'user':
            user_type = self.request.get('user_type')
            banned_from_comments = self.request.get('banned_from_comments')
            banned_from_posting = self.request.get('banned_from_posting')

            cache = buscar(id_object, 'user_cache')
            if cache and user_type and banned_from_comments and banned_from_posting:
                cache.user_type = user_type
                cache.banned_from_posting = banned_from_posting
                cache.banned_from_comments = banned_from_comments
                cache.state = True
                cache.put()
                self.redirect('/admin')
            else:
                self.redirect('/admin')
    #     elif query == 'post_reposrted_cache':
    #         pass
        

#encuentra los post o usuario y comentario por el id
def buscar(id_elemento, elemento):
    cache = memcache.get(elemento)
    if id_elemento in cache:
        return cache[id_elemento]




# convierte el objeto de la base de datos a una diccionario lejible para json  
def diccionarisarcache(info,cual):
    informacion={}
    #info es la cache creada solo con la informacion de echa
    if cual == 'comments_cache':
        for partes in info:
            if info[partes].reported == True and info[partes].state == False:
                informacion[str(info[partes].key().id())]={'comment_id':str(info[partes].key().id()),
                                                          'title':info[partes].title,
                                                          'content':info[partes].content,
                                                          'post':info[partes].post,
                                                          'submitter':info[partes].submitter,
                                                          'created':info[partes].created.strftime('%y/%m/%d'),
                                                          'reported':info[partes].reported,
                                                          'razon':info[partes].razon,
                                                        }
    elif cual == 'post_cache':
        for partes in info:
            if info[partes].modificable == 'pending' and info[partes].state == False:
                informacion[str(info[partes].key().id())]={'post_id':str(info[partes].key().id()),
                                                          'topic':info[partes].topic,
                                                          'title':info[partes].title,
                                                          'content':info[partes].post,
                                                          'post':info[partes].post,
                                                          'submitter':info[partes].submitter,
                                                          'created':info[partes].created.strftime('%y/%m/%d'),
                                                          'modificable':info[partes].modificable,
                                                          'razon':info[partes].razon
                                                        }
    elif cual == 'user_cache':
        for partes in info:
            if info[partes].solicitud_cambio == True and info[partes].state == False:
                informacion[str(info[partes].key().id())]={"userid":str(info[partes].key().id()),
                                                "user_type":info[partes].user_type,
                                                "user_id":info[partes].user_id,
                                                "displayName":info[partes].displayName,
                                                "solicitud_cambio":info[partes].solicitud_cambio,
                                                "rason_solicitud_cambio":info[partes].rason_solicitud_cambio,
                                                "banned_from_comments":info[partes].banned_from_comments,
                                                "banned_from_posting":info[partes].banned_from_posting
                                                        }
    return informacion                    
# crea el query deacuerdo ala info pedidad por el admin
# def createquerty(content):
#     # comentario reportados
#     if content == "comments_cache":
#         comments = {}
#         banned_comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created desc")
#         for p in banned_comments:
#             comments[str(p.key().id())] = p
#         memcache.set("comments_cache", comments)
#         # logging.error(comments)
#         return comments

#     #solicitud de modiicar un post post
#     elif content == 'post_cache':
#         post ={}
#         post_modificables =  db.GqlQuery("SELECT * FROM Post ORDER BY created desc")
#         for p in post_modificables:
#             post[str(p.key().id())] = p
#         memcache.set("post_cache", post)
#         return post

#     # permisos para usuarios
#     elif content == 'user_permisos_cache':
    
#         users ={}

#         users_modificables =  db.GqlQuery("SELECT * FROM User ORDER by user_id")


#         for p in users_modificables:
#             users[str(p.key().id())] = p
#         memcache.set("user_cache", users)
#         return users



