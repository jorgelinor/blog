import handler
import hashlib
import re
import time
from message import Message
from google.appengine.api import memcache
from google.appengine.ext import ndb
from user import User
import logging
from post import Post
from google.appengine.ext import db 
from google.appengine.ext import blobstore 
from google.appengine.ext.webapp import blobstore_handlers 

 
class UserPhoto(ndb.Model): 
    user = ndb.StringProperty() 
    blob_key = ndb.BlobKeyProperty()


class PhotoUploadHandler(handler.Handler,blobstore_handlers.BlobstoreUploadHandler): 
    def post(self,user=None): 
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
        try: 
            upload = self.get_uploads()[0] 
            user_photo = UserPhoto( 
                user=str(user.key().id()), 
                blob_key=upload.key()) 
            user_photo.put() 
            user.img = str(upload.key())
            user.put()
            memcache.delete('user_'+self.request.cookies.get('user_id').split('|')[0])
            time.sleep(2)
            self.redirect('/profile') 

        except: 
            self.redirect('/newpost')

class Profile(handler.Handler):
    #Handler que presenta la pagina del perfil propio, con toda la informacion para ver y cambiar
    def get(self,modificable=False,profile=None,messages=None):
        user = None
        upload_url = blobstore.create_upload_url('/upload_photo')
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)#Los mensajes para mandarlos a la bandeja
        if not self.request.get("u"):#Si no se va a ver el perfil de otra persona
            if not user:#Y no hay cookie
                self.redirect("/login")#para el login
            else:#de lo contrario
                profile = user#se condiciona para entrar a mi perfil
                modificable = True
        else:
            profile = self.get_data("displayName_"+self.request.get("u"),db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1))#Obtener el objeto y a la vez ponlo en el cache
            if len(profile)>0:#si se va a ver el perfil de alguien
                profile = profile[0]
                if user and str(profile.key().id()) == str(user.key().id()):#si el que se va a ver es mi perfil
                    self.redirect("/profile")#accede al primer paso
            elif self.request.get("u") == "ti":
                self.redirect("/profile")
            else:
                self.redirect('/error?e=profile-notfound')#si el perfil no se encuentra da error
        self.render("profile.html",pagename='Perfil',user=user, profile=profile,modificable=modificable,recent_msg=messages,img=profile,upload_url=upload_url)


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler): 
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
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])#obtiene el objeto con la informacion del usuario a editar
            date_pre = self.get_data('create_date',create_date())#creacion de los datos para la fecha,como el procedimiento usa loop lo almaceno en cache para evitar usar el loop nuevamente
            messages = self.GetMessages(actualizar=False,persona=user)#Los mensajes para la bandeja
            self.render("editprofile.html",pagename='Editar Perfil', user=user,years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2],recent_msg=messages)
        else:
            self.redirect('/login')
   
    def post(self):
        #se toman los datos nuevos del usuario
        nickname = valid_username(self.request.get('nickname'))
        actual_password = self.request.get('actualpassword')#para tomar la contrasenia introducida y compararla con la actual
        tel = valid_tel(self.request.get('tel'))
        date = self.request.get('date1')+'-'+self.request.get('date2')+'-'+self.request.get('date3')
        description = self.request.get('description')
        permisos_cambio = self.request.get('solicitar')
        rason_de_solicitud = self.request.get('rason')
        

        #y aqui empieza la verificacion
        user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
        messages = self.GetMessages(actualizar=False,persona=user)
        if not self.verify_edition(user,nickname,tel,date,actual_password)[0]:#el procedimiento de verificacion se define en handler.py, si no cumplese renderiza con errores
            date_pre = self.get_data('create_date',create_date())
            unused,erroruser,errortel,errordesc,errordate,passerror = self.verify_edition(user,nickname,tel,date,actual_password)
            self.render('editprofile.html',pagename='Editar Perfil',user=user,dateerror=errordate, erroruser=erroruser,errortel=errortel,date=user.user_date.split("-"),
                years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2],passerror=passerror,recent_msg=messages)
        else:#de lo contrario, se establecen los nuevos datos al usuario
            user.displayName=nickname[1]
            user.user_tel=tel[1]
            user.user_date=date
            user.user_desc=description
            if permisos_cambio == 'True':
                logging.error('entar', permisos_cambio)
                user.solicitud_cambio = True
            user.rason_solicitud_cambio = rason_de_solicitud
            user.put()
            time.sleep(2)
            memcache.delete('user_'+self.request.cookies.get('user_id').split('|')[0])            
            memcache.delete('displayName_'+user.displayName)
            self.redirect('/profile')


def create_date():
    years,months,days = [],[],[]
    for e in range(1,32):
        days.append(e)
    for e in range(1,13):
        months.append(e)
    for e in range(1950,2013):
        years.append(e)
    return (years,months,days)

class EditPass(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)
            self.render("editpass.html",pagename='Editar contrasenia', user=user,recent_msg=messages)
        else:
            self.redirect("/login")
    def post(self):
        user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
        oldpass = valid_pass(self.request.get('oldpass'))
        newpass = valid_pass(self.request.get('newpass'))
        verify = self.request.get('verify') == newpass[1]
        if self.password_edition(user,oldpass,newpass,verify)[0]:
            user.user_pw = hashlib.sha256(newpass[1]).hexdigest()
            user.put()
            self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1],actualizar=True)
            time.sleep(2)
            self.redirect('/profile')
        else:        
            messages = self.GetMessages(actualizar=False,persona=user)
            unused,errorpass,errornew,errorverify = self.password_edition(user,oldpass,newpass,verify)
            self.render('editpass.html',pagename='Editar contrasenia',user=user,errorpass=errorpass,errornew=errornew,errorverify=errorverify,recent_msg=messages)

class ViewPosts(handler.Handler):
    def get(self,messages=None,mios=False):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)
        if self.request.get('post').isdigit():
            post = Post.get_by_id(int(self.request.get('post')))
            if post:
                if self.request.get('visible') == '0':
                    post.visible = False
                elif self.request.get('visible') == '1':
                    post.visible = True
                post.put()
        if self.request.get("u"):
            profile = self.get_data("displayName_"+self.request.get("u"),db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1))#la informacion del perfil que estoy viendo
            profile = list(profile)
            if len(profile) > 0:#si se encontro
                posts = self.get_data("posts_by_"+profile[0].user_id,db.GqlQuery("select * from Post where submitter='"+profile[0].user_id+"' order by created desc"))#me enlista sus posts
                posts = self.display_names(user,list(posts))
                if user.user_id == profile[0].user_id:
                    mios = True
                self.load_data(lim=5,mios=mios,pagename="Ver posts",posts=posts)
            else:
                self.redirect("/error?e=profile-notfound")
        else:
            if user:
                messages = self.GetMessages(actualizar=False,persona=user)
                posts = self.get_data("posts_by_"+user.user_id,db.GqlQuery("select * from Post where submitter='"+user.user_id+"' order by created desc"))
                posts = self.display_names(user,list(posts))
                self.load_data(lim=5,mios=True,pagename="Ver posts",posts=posts) 
            else:
                self.redirect("/login")

class ViewComments(handler.Handler):
    def get(self,author=None,mios=False,comments=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:#Verificacion de la cookie
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])#informacion del usuario logueado
            messages = self.GetMessages(actualizar=False,persona=user)#los mensajes
            if self.request.get("u"):#si hay query
                profile = self.get_data("displayName_"+self.request.get("u"),db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1))#busca el dueno de los comentarios
                if len(profile) == 1:#y si existe
                    comments = self.get_data("comments_by_"+profile[0].user_id,db.GqlQuery("select * from Comment where submitter='"+profile[0].user_id+"' order by created desc"))#enlista sus comentarios
                    comments = self.display_names(user,list(comments))#camufla los nombres
                    if user.displayName == self.request.get("u"):#si son mios
                        mios = True
                    else:#son de alguien mas
                        author = self.request.get("u")
                else:
                    self.redirect('/error?e=profile-notfound')
            else:   
                mios = True
                comments = self.get_data("comments_by_"+user.user_id,db.GqlQuery("select * from Comment where submitter='"+user.user_id+"' order by created desc"))#busca solo mis comentarios
                comments = self.display_names(user,list(comments))#ponles 'ti'
            self.render("just_comments.html",pagename='Ver comentarios',mios=mios,author=author,user=user,comments=comments,recent_msg=messages)
        else:
            self.redirect("/login")

class SendPm(handler.Handler):#para enviar mensajes
    def get(self,messages=None,target=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)
            if self.request.get("u"):#si hay a quien mandar mensaje
                destination = self.get_data("displayName_"+self.request.get("u"),db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1))#Busca el destino
                if len(destination) > 0:#si existe
                    target = destination[0]#sera target ahora
                    if target.user_id == user.user_id:#Si soy yo mismo
                        self.redirect('/error?e=self-messaging')# los mensajes para la bandeja
                else:
                    self.redirect('/error?e=profile-notfound')
            else:
                self.redirect("/")
        else:
            self.redirect('/login')
        self.render("sendpm.html",user=user,target=target,pagename="Mensaje Privado",recent_msg=messages)#target es el objeto del perfil a quien se mandara el mensaje

    def post(self):
        user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
        subject = self.request.get("pmtitle")
        messages = self.GetMessages(actualizar=False,persona=user)
        if not subject:
            subject = "Sin asunto"
        content = self.request.get("pmcontent")
        destination = self.get_data("displayName_"+self.request.get("u"),db.GqlQuery("select * from User where displayName='"+self.request.get("u")+"'").fetch(1))[0]#El objet del usuario sera el destino
        submitter = user.user_id
        if not content:
            self.render("sendpm.html",user=user,target=destination.user_id,pagename="Mensaje Privado",error="Mensaje requerido",recent_msg=messages)
        else:
            msg = Message(submitter=submitter,destination=destination.user_id,subject=subject,content=content)
            msg.put()
            self.GetMessages(actualizar=True,persona=destination)
            self.redirect("/profile?u="+self.request.get("u"))