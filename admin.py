# -*- coding: utf-8 -*-
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
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            if user.user_type == "admin":
                messages = self.GetMessages(persona=user)
                self.render("admin.html", pagename=u"Administración",user=user,recent_msg=messages)
            else:
                self.redirect('/posts/news')
        else:
            self.redirect("/login")

class Admin_info(handler.Handler):
    def get(self):
        # los querys deben ser comments_reported_cache o 
        # post_modificable_cache o user_permisos_cache o post_reposrted_cache
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))

            if user.user_type == "admin":
                info={}
                action = self.request.GET.get('action')
                informacion = memcache.get(action)
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
                self.redirect('/posts/news')
        else:
            self.redirect('/login')

class Users(handler.Handler):
    def get(self):
        user_cache()
        user = self.request.get('user')
        topicos = buscar_user_tipe(user)
        informacion = diccio(topicos,'user_cache')
        self.write(json.dumps(informacion))


class Topicos(handler.Handler):
    def get(self):
        post_cache()
        topi= self.request.get('topico')
        logging.error(topi)
        topicos = buscar_topico(topi,'post_cache')
        informacion = diccio(topicos,'post_cache')
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
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            if user.user_type == "admin":
                admin2 = False
                query=''
                ins, id_object = id_obj.split('_')[0], id_obj.split('_')[1]
                if ins == 'come':
                    query='comments_cache'
                elif ins == 'post':
                    query='post_cache'
                elif ins == 'user':
                    query='user_cache'
                elif ins == 'post2':
                    admin2 = True
                    query='post_cache'


                info = buscar(id_object , query)
                self.render('upload.html',admin2=admin2,info=info, query=query,user=user,pagename=u'Administración')
            else:
                self.redirect('/posts/news')
        else:
            self.redirect('/login')

    def post(self, id_obj):
        ins, id_object = id_obj.split('_')[0], id_obj.split('_')[1]
        if ins == 'come':
            # coment_id = self.request.get('comment_id')
            comments_reported = self.request.get('report')
            cache = buscar(id_object, 'comments_cache')
            if cache and comments_reported == 'accept-report':
                com=Comment.get_by_id(int(id_object))
                if com and com.reported == True:
                    post = Post.get_by_id(int(com.post))
                    post.comments -= 1
                    post.put()
                    com.delete()
                    time.sleep(2)
                    self.get_data('Comment','dict',com.key().id(),None,actualizar=True)
                    self.get_data('Post','dict',post.key().id(),post,actualizar=True)
                    comments_cache()
                else:
                    comments_cache()
                self.redirect('/admin')
            elif cache and comments_reported == 'deny-report':
                com = Comment.get_by_id(int(id_object))
                if com and com.reported == True:
                    com.reported=False
                    com.razon=[]
                    com.put()
                    time.sleep(2)
                    comments_cache()
                self.redirect('/admin')

        elif ins == 'post':
            modificable = self.request.get('permiso')
            mensaje_titulo = ''
            mensaje_contenido = ''
            if eval(modificable) == True:
                mensaje_titulo = '<h3 style="color:green">PEDIDO ACEPTADO</h3>'
                mensaje_contenido = '* Su pedido para modificar <a href="/'+id_object+'">este</a> post fue aceptado'
            elif eval(modificable) == False:
                mensaje_titulo = '<h3 style="color:red">PEDIDO DENEGADO</h3>'
                mensaje_contenido = '* Su pedido para modificar <a href="/'+id_object+'">este</a> post fue rechazado'
            cache = buscar(id_object, 'post_cache')
            if cache and cache.modificable == 'pending' and modificable:
                cache.modificable = modificable
                cache.state = False
                cache.razon = None
                cache.put()
                msg = Message(submitter=u'Administración',destination=cache.submitter,subject=mensaje_titulo,content=mensaje_contenido)
                msg.put()
                time.sleep(2)
                post_cache()
                self.get_data('Post','dict',cache.key().id(),cache,actualizar=True)
                Message.update(cache.submitter,msg)
                self.redirect('/admin')
            else:
                self.redirect('/admin')
        elif ins == 'post2':
            accion = self.request.get('action')
            cache = buscar(id_object, 'post_cache')
            if accion == 'borrar' and cache and cache.modificable != 'pending':
                comentarios = Comment.by_post(id_object)
                for coment in comentarios:
                    self.get_data('Comment','dict',int(coment.key().id()),None,actualizar=True)
                    coment.delete()
                self.get_data('Post','dict',cache.key().id(),None,actualizar=True)
                cache.delete()
                msg = Message(submitter=u'Administración',destination=cache.submitter,subject='<h3 style="color:red">IMPORTANTE</h3>',content='* Se ha eliminado un post de su propiedad por contenido sexual,racismo...')
                msg.put()
                time.sleep(2)
                Message.update(cache.submitter,msg)
                post_cache()
                comments_cache()
            elif accion == 'ocultar' and cache and cache.modificable != 'pending':
                cache.visible = False
                cache.modificable = 'True'
                cache.put()
                msg = Message(submitter=u'Administración',destination=cache.submitter,subject='<h3 style="color:red">IMPORTANTE</h3>',content='* Se ha ocultado un post de su propiedad por contenido sexual,racismo...')
                msg.put()
                time.sleep(2)
                self.get_data('Post','dict',cache.key().id(),cache,actualizar=True)
                Message.update(cache.submitter,msg)
                post_cache()
            elif accion == 'advertir' and cache and cache.modificable != 'pending':
                cache.modificable = 'True'
                cache.put()
                msg = Message(submitter=u'Administración',destination=cache.submitter,subject='<h3 style="color:red">IMPORTANTE</h3>',content='* Su <a href="/'+id_object+'">post</a> tiene contenido sexual,racismo... editelo o sera eliminado/ocultado.')
                msg.put()
                time.sleep(2)
                self.get_data('Post','dict',cache.key().id(),cache,actualizar=True)
                Message.update(cache.submitter,msg)
                post_cache()
            self.redirect('/admin')

        elif ins == 'user':
            user_type = self.request.get('user_type')
            banned_from_comments = self.request.get('banned_from_comments')
            banned_from_posting = self.request.get('banned_from_posting')
            cache = buscar(id_object, 'user_cache')
            if cache and user_type and banned_from_comments and banned_from_posting:
                cache.user_type = user_type
                cache.banned_from_posting = eval(banned_from_posting)
                cache.banned_from_comments = eval(banned_from_comments)
                rason_solicitud_cambio = None
                solicitud_cambio = False
                cache.state = True
                cache.put()
                time.sleep(2)
                self.get_data('User','dict',cache.key().id(),cache,actualizar=True)
                user_cache()
                self.redirect('/admin')
            else:
                self.redirect('/admin')
        

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


def diccio(info,cual):
    informacion={}
    if cual == 'post_cache':
        for partes in info:
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



