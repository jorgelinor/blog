#Esta es la clase principal, la cual hereda a la mayoria de las demas.

import webapp2 
import os
import jinja2
from google.appengine.api import memcache
from google.appengine.ext import db
import logging
import hashlib
from user import User

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
    def GetMessages(self,actualizar,persona):
        messages = memcache.get(persona.user_id+"_mensajes")
        if actualizar == True or messages == None:
            messages = db.GqlQuery("select * from Message where destination='"+persona.user_id+"' order by date desc")
            memcache.add(persona.user_id+"_mensajes",messages)
        messages = list(messages)
        for e in messages:
            if e.submitter != "Administracion":
                e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
        return messages

    #este metodo es super util a la hora de obtener cache, toma dos parametros (key,funcion) donde si la key no existe en el cache, se ejecuta
    #la funcion y se hace cache para la proxima peticion
    def get_data(self,key,query,actualizar=False):
        data = memcache.get(key)
        if data == None or actualizar==True:
            data = query
            self.write('algo')
            memcache.add(key, data)
        return data

    #Este es el metodo de verificacion de cookie que toma una cookie y si es completamente valida, retorna una tupla (True,objeto)
    def get_cookie_user(self,cookie):
        if cookie:
            if cookie.split("|")[0].isdigit():
                if hashlib.sha256(cookie.split("|")[0]).hexdigest() == cookie.split("|")[1]:
                    if User.get_by_id(int(cookie.split("|")[0])):
                        return (True,User.get_by_id(int(cookie.split("|")[0])))
        return (False,None)

    #Metodo de verificacion en login, toma todas las condicionales como parametros y si cumplen se manda (True,error de contrasenia,error de usuario) para saber si es valido
    def verify_login(self,user=None,pw=None,query=[]):
        erroruser,errorpass='',''
        if not(user[0] and pw[0] and len(query)>0 and query[0].user_pw == hashlib.sha256(pw[1]).hexdigest()):
            if not user[0]:
                erroruser = 'Usuario invalido'
            if len(query)<1:
                erroruser = "Este usuario no existe"
            if not pw[0]:
                errorpass = 'Contrasenia incorrecta'
            if len(query)>0 and query[0].user_pw != hashlib.sha256(pw[1]).hexdigest():
                errorpass = "Contrasenia invalida"
            return (False,errorpass,erroruser)
        return (True,errorpass,erroruser)

    def verify_edition(self,user=None,nick=None,tel=[],date='',actual_pw=''):
        erroruser,errortel,errordesc,errordate,passerror='','','','',''
        actualnick = self.get_data("displayName_"+nick[1],db.GqlQuery("select * from User where displayName='"+nick[1]+"'").fetch(1))
        check_pw = False
        check_nick = True
        if hashlib.sha256(actual_pw).hexdigest()==user.user_pw:
            check_pw = True
        if len(actualnick) == 1:
            if actualnick[0].displayName != user.displayName:
                check_nick = False
        if (not nick[0]) or (not tel[0]) or (len(date)<7) or (check_pw == False) or (check_nick == False):
            if not nick[0]:
                erroruser = 'Nombre invalido'
            if not tel[0]:
                errortel = 'Numero invalido'
            if not len(date)>7:
                errordate = 'Fecha invalida'
            if check_pw ==False:
                passerror = 'Contrasena erronea'
            if check_nick == False:
                erroruser = 'Nombre tomado'
            return (False,erroruser,errortel,errordesc,errordate,passerror)
        return (True,erroruser,errortel,errordesc,errordate,passerror)

    def display_names(self,user=None,lista=[]):
        for e in lista:
            if user and e.submitter == user.user_id:
                e.submitter = "ti"
            else:
                submitter = self.get_data('submitter_'+e.submitter,db.GqlQuery("select * from User where user_id='"+e.submitter+"'"))
                submitter = list(submitter)
                if len(submitter) < 1:
                    e.submitter = e.submitter+"|False"
                else:
                    e.submitter = submitter[0].displayName
        return lista

    def password_edition(self,user,oldpass,newpass,verify):
        errorpass,errornew,errorverify = '','',''
        if oldpass[0]:
            if user.user_pw == hashlib.sha256(oldpass[1]).hexdigest():
                if newpass[0]:
                    if verify:
                        return (True,errorpass,errornew,errorverify)
                    else:
                        errorverify = "Passwords doesn't match"
                else:
                    errornew = 'Invalid password'
            else:
                errorpass = 'Incorrect password'
        else:
            errorpass = 'Invalid password'
        return (False,errorpass,errornew,errorverify)

class ErrorHandler(Handler):
    def get(self,error='',messages=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
        	user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
        	messages = self.GetMessages(actualizar=False,persona=user)
        query = self.request.get('e')
        if query == "profile-notfound":
            error = 'Perfil no encontrado.'
        if query == 'already-logged':
            error = 'Ya estas logueado.'
        if query == 'already-registered':
            error = 'Ya estas registrado.'
        if query == 'self-messaging':
        	error = 'No puedes enviarte un mensaje a ti mismo.'
        if query == 'post-notfound':
            error = 'Este post no existe.'
        if query == 'comment-notfound':
            error = 'Este comentario no existe o no pertenece a este post.'
        if query == 'not-yourpost':
            error = 'Este post no te pertenece.'
        self.render('error.html',user=user,pagename='Error',error=error, recent_msg=messages)

class Stats(Handler):
    def get(self,messages=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)
        animales = self.get_data("cantidad_Animales",len(list(db.GqlQuery("select * from Post where topic='Animales'"))))
        tecnologia = self.get_data("cantidad_Tecnologia", len(list(db.GqlQuery("select * from Post where topic='Tecnologia'"))))
        preguntas = self.get_data("cantidad_Preguntas", len(list(db.GqlQuery("select * from Post where topic='Preguntas'"))))
        musica = self.get_data("cantidad_Musica", len(list(db.GqlQuery("select * from Post where topic='Musica'"))))
        programacion = self.get_data("cantidad_Programacion", len(list(db.GqlQuery("select * from Post where topic='Programacion'"))))
        self.render("graficos.html",pagename="Stats de la pagina", t1=animales,t2=tecnologia,t3=preguntas,t4=musica,t5=programacion,user=user,recent_msg=messages)