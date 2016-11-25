#Esta es la clase principal, la cual hereda a la mayoria de las demas.
# -*- coding: utf-8 -*-
import webapp2 
import os
import jinja2
from google.appengine.api import memcache
from google.appengine.ext import db
import logging
import hashlib
from user import User
from post import *
from comment import *
from likes import *
from message import Message
import json

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
                                       
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)
    def render_str(self,template,**params):
        y = jinja_env.get_template(template)
        return y.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    #Actualizar solo sera True, y correra el query, cuando alguien manda un nuevo mensaje
    def GetMessages(self,persona):
        if persona:
            messages = memcache.get("Message")
            if messages == None:
                messages = {persona.user_id:list(db.GqlQuery("select * from Message where destination='%s'"%persona.user_id))}
                memcache.set("Message",messages)
            messages_persona = messages.get(persona.user_id)
            if messages_persona == None:
                msgs = list(db.GqlQuery("select * from Message where destination='%s'"%persona.user_id))
                messages[persona.user_id] = msgs
                memcache.set('Message',messages)
            return self.display_names(persona,memcache.get('Message').get(persona.user_id))




    #este metodo es super util a la hora de obtener cache, toma dos parametros (key,funcion) donde si la key no existe en el cache, se ejecuta
    #la funcion y se hace cache para la proxima peticion
    def get_data(self,key_cache,list_or_dict='dict',key=None,query=None,actualizar=False):
        data = memcache.get(key_cache)
        if not data:
            data_dict = {}
            data_list = db.GqlQuery('SELECT * FROM %s' % key_cache)
            if key_cache == 'Post':
                data_list = db.Query(Post).order('-created')
            data_list = list(data_list)
            for ob in data_list:
                data_dict[ob.key().id()] = ob
            data = {key_cache+'_list':data_list,key_cache+'_dict':data_dict}
            memcache.add(key_cache,data)
        if actualizar==True:
            logging.error('test')
            test = data[key_cache+'_dict'].get(key)
            if query:
                data[key_cache+'_dict'][key] = query
            else:
                del data[key_cache+'_dict'][key]
            if not test:
                data[key_cache+'_list'].insert(0,query)
            else:
                lista = data[key_cache+'_list']
                for indice in range(len(lista)):
                    if lista[indice].key().id() == key:
                        if query:
                            lista[indice] = query
                            logging.error('lol')
                        else:
                            logging.error('lal')
                            del lista[indice]
                data[key_cache+'_list'] = lista
            memcache.set(key_cache, data)
        return data[key_cache+'_'+list_or_dict]

    def to_dict(self,lista):
        dic = {}
        if lista:
            for e in lista:
                dic[e.key().id()] = e
        return dic

    def to_list(self,dic,match=None):
        lista = []
        if dic:
            for e in dic:
                if match:
                    if dic[e].post == match:
                        lista.append(dic[e])
                else:
                    lista.append(dic[e])
        return lista

    #Este es el metodo de verificacion de cookie que toma una cookie y si es completamente valida, retorna una tupla (True,objeto)
    def get_cookie_user(self,cookie):
        if cookie:
            if cookie.split("|")[0].isdigit():
                if hashlib.sha256(cookie.split("|")[0]).hexdigest() == cookie.split("|")[1]:
                    if User.get_by_id(int(cookie.split("|")[0])):
                        return (True,User.get_by_id(int(cookie.split("|")[0])))
        return (False,None)

    #Metodo de verificacion en login, toma todas las condicionales como parametros y si cumplen se manda (True,error de contrasenia,error de usuario) para saber si es valido
    def verify_login(self,user=None,pw=None,query=None):
        erroruser,errorpass='',''
        if not(user[0] and pw[0] and query and query.user_pw == hashlib.sha256(pw[1]).hexdigest()):
            if not user[0]:
                erroruser = u'Usuario inválido'
            if not query:
                erroruser = u"Este usuario no exíste"
            if not pw[0]:
                errorpass = u'Contraseña incorrecta'
            if query and query.user_pw != hashlib.sha256(pw[1]).hexdigest():
                errorpass = u"Contraseña inválida"
            return (False,errorpass,erroruser)
        return (True,errorpass,erroruser)

    def verify_signup(self,username,email,nick,tel,date,pw,verify,user,user1):
        erroruser,errordisplay,errormail,errorpass,errorverify,errortel,errordesc,errordate='','','','','','','',''

        if not(username[0] and nick[0] and tel[0] and len(date)>7 and pw[0] and verify and email[0] and not (user and user1)):
            if not nick[0]:
                errordisplay = u'Nombre inválido'
            if user1:
                errordisplay = 'Nombre tomado'
            if not username[0]:
                erroruser = u'Nombre de usuario inválido'
            if user:
                erroruser = u'Este usuario ya exíste'
            if not pw[0]:
                errorpass = u'Contraseña inválida'
            if not verify:
                errorverify = u"Las contraseñas no coinciden"
            if not tel[0]:
                errortel = u'Introduce un número de teléfono'
            if not len(date)>7:
                errordate = u'Fecha inválida'
            if not email[0]:
                errormail = u'Correo electrónico inválido'
            return (False,erroruser,errordisplay,errormail,errorpass,errorverify,errortel,errordesc,errordate)
        return (True,erroruser,errordisplay,errormail,errorpass,errorverify,errortel,errordesc,errordate)

    def verify_edition(self,user=None,nick=None,tel=[],date='',actual_pw=''):
        erroruser,errortel,errordesc,errordate,passerror='','','','',''
        check_pw = False
        check_nick = True
        if hashlib.sha256(actual_pw).hexdigest()==user.user_pw:
            check_pw = True
        if User.by_nickname(nick[1]):
            if nick[1] != user.displayName:
                check_nick = False
        if (not nick[0]) or (not tel[0]) or (len(date)<7) or (check_pw == False) or (check_nick == False):
            if not nick[0]:
                erroruser = u'Nombre inválido'
            if not tel[0]:
                errortel = u'Número inválido'
            if not len(date)>7:
                errordate = u'Fecha inválida'
            if check_pw ==False:
                passerror = u'Contraseña errónea'
            if check_nick == False:
                erroruser = u'Nombre tomado'
            return (False,erroruser,errortel,errordesc,errordate,passerror)
        return (True,erroruser,errortel,errordesc,errordate,passerror)

    def display_names(self,user=None,lista=[]):
        for e in lista:
            if user and e.submitter == user.user_id:
                e.submitter = "ti"
            else:
                submitter = User.by_username(e.submitter)
                if e.submitter != "ti" and e.submitter != "Administracion":
                    if not submitter:
                        e.submitter = e.submitter+"|False"
                    else:
                        e.submitter = submitter.displayName
        return lista

    def password_edition(self,user,oldpass,newpass,verify):
        errorpass,errornew,errorverify = '','',''
        if oldpass[0]:
            if user.user_pw == hashlib.sha256(oldpass[1]).hexdigest():
                if newpass[0]:
                    if verify:
                        return (True,errorpass,errornew,errorverify)
                    else:
                        errorverify = u"Las contraseñas no coinciden"
                else:
                    errornew = u'Contraseña inválida'
            else:
                errorpass = u'Contraseña incorrecta'
        else:
            errorpass = u'Contraseña incorrecta'
        return (False,errorpass,errornew,errorverify)
    def make_json_data(self,posts=None,mios=None,user=None):
        index = {}
        for e in posts:
            user_ac = User.by_nickname(e.submitter.split('|')[0],user)
            if e.visible != False or e.visible==False and mios==True: #antes de mandar el json, revisa si los posts son visibles o no, para luego reenderizarlos correctamente
                obj = {}
                obj["id"] = e.key().id()
                obj["title"] = e.title
                obj["post"] = e.post
                obj["submitter"] = e.submitter
                obj["created"] = str(e.created)
                obj["created_str"] = e.created_str
                obj["modificable"] = e.modificable
                obj["razon"] = e.razon
                if e.submitter == 'ti':
                    obj["options"] = True
                else:
                    obj["options"] = False
                if e.comments > 1:
                    obj["comments"] = str(e.comments)+' comentarios'
                elif e.comments == 1:
                    obj["comments"] = str(e.comments)+' comentario'
                else:
                    obj['comments'] = ''
                obj["visible"] = e.visible
                if user_ac.img:
                    obj["submitter_img"] = '/view_photo/'+user_ac.img
                else:
                    obj["submitter_img"] = '/img/profile.jpg'
                index[len(index)] = obj
        return json.dumps(index)

    def load_data(self,messages=None,lim=None,mios=None,pagename=None,posts=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)
        posts = self.display_names(user,posts)
        self.render('page.html',pagename=pagename,posts=posts,user=user,recent_msg=messages,limit=lim,data=self.make_json_data(posts=posts,mios=mios,user=user),mios=mios)

class ErrorHandler(Handler):
    def get(self,error='',messages=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            if user:
                messages = self.GetMessages(persona=user)
        query = self.request.get('e')
        if query == "profile-notfound":
            error = u'Perfíl no encontrado.'
        if query == 'already-logged':
            error = u'Ya estás identificado.'
        if query == 'already-registered':
            error = u'Ya estás registrado.'
        if query == 'self-messaging':
        	error = u'No puedes enviarte un mensaje a tí mismo.'
        if query == 'post-notfound':
            error = u'Este post no existe.'
        if query == 'comment-notfound':
            error = 'Este comentario no existe o no pertenece a este post.'
        if query == 'not-yourpost':
            error = 'Este post no te pertenece.'
        self.render('error.html',user=user,pagename='Error',error=error, recent_msg=messages)

class Stats(Handler):
    def get(self,messages=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            if user.user_type == "admin":
                messages = self.GetMessages(persona=user)
                animales = len(list(Post.by_topic('Animales')))
                tecnologia = len(list(Post.by_topic('Tecnologia')))
                preguntas = len(list(Post.by_topic('Preguntas')))
                musica = len(list(Post.by_topic('Musica')))
                programacion = len(list(Post.by_topic('Programacion')))
                self.render("graficos.html",pagename=u"Stats de la página", t1=animales,t2=tecnologia,t3=preguntas,t4=musica,t5=programacion,user=user,recent_msg=messages)
            else:
                self.redirect('/posts/news')



class Like(Handler):
    def get(self):
        option ="like"
        user_id = self.request.cookies.get('user_id').split('|')[0]
        logging.error=(self.request.GET.get('id_obj'))
        self.write(json.dumps(verificaruser(user_id,self.request.GET.get('id_obj'),option)))

class DisLike(Handler):
    def get(self):
        user = None
        option ='dislike'
        user_id = self.request.cookies.get('user_id').split('|')[0]
        self.write(json.dumps(verificaruser(user_id,self.request.GET.get('id_obj'),option)))
