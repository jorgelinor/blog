# -*- coding: utf-8 -*-
import handler
import hashlib
import re
import time
from message import Message
from google.appengine.api import memcache
from google.appengine.ext import ndb
from user import *
import logging
from post import Post
from google.appengine.ext import db 
from google.appengine.ext import blobstore 
from google.appengine.ext.webapp import blobstore_handlers 
from comment import *

 
class UserPhoto(ndb.Model): 
    user = ndb.StringProperty() 
    blob_key = ndb.BlobKeyProperty()


class PhotoUploadHandler(handler.Handler,blobstore_handlers.BlobstoreUploadHandler): 
    def post(self,user=None): 
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
        try: 
            upload = self.get_uploads()[0] 
            user_photo = UserPhoto( 
                user=str(user.key().id()), 
                blob_key=upload.key()) 
            user_photo.put() 
            user.img = str(upload.key())
            user.put()
            self.get_data('User','dict',user.key().id(),user,actualizar=True)
            time.sleep(2)
            self.redirect('/profile') 

        except: 
            self.redirect('/newpost')

class ChangeBackground(handler.Handler):
    def get(self):
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
        if user:
            color = self.request.get('color')
            img = self.request.get('img')
            if color:
                user.pref_color = color
            elif img:
                user.pref_color = None
            user.put()
            self.get_data('User','dict',user.key().id(),user,actualizar=True)
        self.redirect('/posts/news')
        

class Profile(handler.Handler):
    #Handler que presenta la pagina del perfil propio, con toda la informacion para ver y cambiar
    def get(self,modificable=False,profile=None,messages=None):
        user = None
        upload_url = blobstore.create_upload_url('/upload_photo')
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            if user:
                messages = self.GetMessages(persona=user)#Los mensajes para mandarlos a la bandeja
        if not self.request.get("u"):#Si no se va a ver el perfil de otra persona
            if not user:#Y no hay cookie
                self.redirect("/login")#para el login
            else:#de lo contrario
                profile = user#se condiciona para entrar a mi perfil
                modificable = True
        else:
            profile = User.by_nickname(self.request.get('u'))#Obtener el objeto y a la vez ponlo en el cache
            if profile:#si se va a ver el perfil de alguien
                if user and str(profile.key().id()) == str(user.key().id()):#si el que se va a ver es mi perfil
                    self.redirect("/profile")#accede al primer paso
            elif self.request.get("u") == "ti":
                self.redirect("/profile")
            else:
                self.redirect('/error?e=profile-notfound')#si el perfil no se encuentra da error
        self.render("profile.html",pagename=u'Perfíl',user=user, profile=profile,modificable=modificable,recent_msg=messages,img=profile,upload_url=upload_url)


class ViewPhotoHandler(handler.Handler,blobstore_handlers.BlobstoreDownloadHandler): 
    def get(self, photo_key):
        if not blobstore.get(photo_key): 
            self.error(404) 
        else: 
            self.send_blob(photo_key) 

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if USER_RE.match(username):
        return (True,username)
    else:
        return (False,username)

PASS_RE = re.compile(r"^[a-zA-Z0-9]{3,20}$")
def valid_pass(password):
    if PASS_RE.match(password):
        return (True,password)
    return (False,password)

def valid_tel(tel):
    if not tel:
        return (False,tel)
    if tel.isdigit():
        if len(tel) > 7:
            return (True,tel)
    return (False,tel)

class EditProfile(handler.Handler):
    #Presenta la pagina para edicion de perfil
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:#verificacion de la cookie
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            date_pre = create_date()#creacion de los datos para la fecha,como el procedimiento usa loop lo almaceno en cache para evitar usar el loop nuevamente
            date = str(user.user_date).split('-')
            messages = self.GetMessages(persona=user)#Los mensajes para la bandeja
            self.render("editprofile.html",date=date,pagename=u'Editar Perfíl', user=user,years=date_pre[0],months=date_pre[1],days=date_pre[2],recent_msg=messages)
        else:
            self.redirect('/login')
   
    def post(self):
        #se toman los datos nuevos del usuario
        nickname = valid_display(self.request.get('nickname'))
        actual_password = self.request.get('actualpassword')#para tomar la contrasenia introducida y compararla con la actual
        tel = valid_tel(self.request.get('tel'))
        date = valid_date(self.request.get('date1'))[1]+'-'+valid_date(self.request.get('date2'))[1]+'-'+valid_date(self.request.get('date3'))[1]
        description = self.request.get('description')
        permisos_cambio = self.request.get('solicitar')
        rason_de_solicitud = self.request.get('rason')
        

        #y aqui empieza la verificacion
        user = self.get_data('User')
        user = user.get(int(self.request.cookies.get('user_id').split('|')[0])) 
        messages = self.GetMessages(persona=user)
        if not self.verify_edition(user,nickname,tel,date,actual_password)[0]:#el procedimiento de verificacion se define en handler.py, si no cumplese renderiza con errores
            date_pre = create_date()
            unused,erroruser,errortel,errordesc,errordate,passerror = self.verify_edition(user,nickname,tel,date,actual_password)
            self.render('editprofile.html',pagename=u'Editar Perfíl',user=user,errordate=errordate, erroruser=erroruser,errortel=errortel,date=user.user_date.split("-"),
                years=date_pre[0],months=date_pre[1],days=date_pre[2],passerror=passerror,recent_msg=messages)
        else:#de lo contrario, se establecen los nuevos datos al usuario
            user.displayName=nickname[1]
            user.user_tel=tel[1]
            user.user_date=date
            user.user_desc=description
            if permisos_cambio == 'True':
                logging.error('entar', permisos_cambio)
                user.solicitud_cambio = True
                user.state = False
            user.rason_solicitud_cambio = rason_de_solicitud
            user.put()
            time.sleep(2)
            user_cache()
            self.get_data('User','dict',user.key().id(),user,actualizar=True)
            self.redirect('/profile')

def valid_date(date):
    if not date:
        return (False,'')
    if date.isdigit():
        return (True,date)
    return (False,'')

DISPLAY_RE = re.compile(r"^[a-zA-Z0-9_ -]{3,20}$")
def valid_display(username):
    if DISPLAY_RE.match(username):
        return (True,username)
    else:
        return (False,username)

def create_date():
    years,months,days = [],['Mes'],[u'Día']
    for e in range(1,32):
        days.append(e)
    for e in range(1,13):
        months.append(e)
    for e in range(1950,2013):
        years.append(e)
    years.append(u'Año')
    years = list(reversed(years))
    return (years,months,days)

class EditPass(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)
            self.render("editpass.html",pagename=u'Editar contraseña', user=user,recent_msg=messages)
        else:
            self.redirect("/login")
    def post(self):
        user = self.get_data('User')
        user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
        oldpass = valid_pass(self.request.get('oldpass'))
        newpass = valid_pass(self.request.get('newpass'))
        verify = self.request.get('verify') == newpass[1]
        if self.password_edition(user,oldpass,newpass,verify)[0]:
            user.user_pw = hashlib.sha256(newpass[1]).hexdigest()
            user.put()
            self.get_data('User','dict',user.key().id(),user,actualizar=True)
            time.sleep(2)
            self.redirect('/profile')
        else:        
            messages = self.GetMessages(persona=user)
            unused,errorpass,errornew,errorverify = self.password_edition(user,oldpass,newpass,verify)
            self.render('editpass.html',pagename=u'Editar contraseña',user=user,errorpass=errorpass,errornew=errornew,errorverify=errorverify,recent_msg=messages)

class ViewPosts(handler.Handler):
    def get(self,messages=None,mios=False):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)
        if self.request.get('post').isdigit():
            post = Post.get_by_id(int(self.request.get('post')))
            if post:
                if self.request.get('visible') == '0':
                    post.visible = False
                elif self.request.get('visible') == '1':
                    post.visible = True
                post.put()
                self.get_data('Post','dict',post.key().id(),post,actualizar=True)
                self.redirect("/profile/_viewposts")
        if self.request.get("u"):
            profile = User.by_nickname(self.request.get('u'))
            if profile:#si se encontro
                posts = Post.by_owner(profile.user_id)
                if user.user_id == profile.user_id:
                    mios = True
                self.load_data(lim=5,mios=mios,pagename="Ver posts",posts=posts)
            else:
                self.redirect("/error?e=profile-notfound")
        else:
            if user:
                messages = self.GetMessages(persona=user)
                posts = Post.by_owner(user.user_id)
                self.load_data(lim=5,mios=True,pagename="Ver posts",posts=posts) 
            else:
                self.redirect("/login")

class ViewComments(handler.Handler):
    def get(self,author=None,mios=False,comments=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:#Verificacion de la cookie
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)#los mensajes
            if self.request.get("u"):#si hay query
                profile = User.by_nickname(self.request.get('u'))
                if profile:#y si existe
                    comments = Comment.busqueda_comment(profile.user_id)
                    comments = self.display_names(user,comments)#camufla los nombres
                    if user.displayName == self.request.get("u"):#si son mios
                        mios = True
                    else:#son de alguien mas
                        author = self.request.get("u")
                else:
                    self.redirect('/error?e=profile-notfound')
            else:   
                mios = True
                comments = Comment.busqueda_comment(profile.user_id)
                comments = self.display_names(user,list(comments))#ponles 'ti'
            self.render("just_comments.html",pagename='Ver comentarios',mios=mios,author=author,user=user,comments=comments,recent_msg=messages)
        else:
            self.redirect("/login")

class SendPm(handler.Handler):#para enviar mensajes
    def get(self,messages=None,target=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)
            if self.request.get("u"):#si hay a quien mandar mensaje
                target = User.by_nickname(self.request.get('u'))
                if target:#si existe
                    if target.user_id == user.user_id:#Si soy yo mismo
                        self.redirect('/error?e=self-messaging')# los mensajes para la bandeja
                else:
                    self.redirect('/error?e=profile-notfound')
            else:
                self.redirect('/posts/news')
        else:
            self.redirect('/login')
        self.render("sendpm.html",user=user,target=target,pagename="Mensaje Privado",recent_msg=messages)#target es el objeto del perfil a quien se mandara el mensaje

    def post(self):
        user = self.get_data('User')
        user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
        subject = self.request.get("pmtitle")
        messages = self.GetMessages(persona=user)
        if not subject:
            subject = "Sin asunto"
        content = self.request.get("pmcontent")
        destination = User.by_nickname(self.request.get('u'))
        submitter = user.user_id
        if not content:
            self.render("sendpm.html",user=user,target=destination.user_id,pagename="Mensaje Privado",error="Mensaje requerido",recent_msg=messages)
        else:
            msg = Message(submitter=submitter,destination=destination.user_id,subject=subject,content=content)
            msg.put()
            Message.update(destination.user_id,msg)
            self.redirect("/profile?u="+self.request.get("u"))