#Clase de registro
# -*- coding: utf-8 -*-
import random
import string
import handler
from user import User
import hashlib
import re
from google.appengine.ext import db
from google.appengine.api import memcache

class Signup(handler.Handler):
    def get(self):
        user = None
        date_pre = create_date()
        if not self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            self.render('signup.html',pagename='Registrar',url='Signup',link='/',years=date_pre[0],months=date_pre[1],days=date_pre[2])
        else:
            self.redirect("error?e=already-registered")
        
    def post(self,user_ob=None,user_ob1=None):
        username = valid_username(self.request.get('username'))
        password = valid_pass(self.request.get('password'))
        displayName = valid_display(self.request.get('displayName'))
        tel = valid_tel(self.request.get('tel'))
        date = valid_date(self.request.get('date1'))[1]+'-'+valid_date(self.request.get('date2'))[1]+'-'+valid_date(self.request.get('date3'))[1]
        description = self.request.get('description')
        verify = self.request.get('verify')==self.request.get('password')
        email = valid_email(self.request.get('email'))
        user_ob = User.by_username(username[1])
        user_ob1 = User.by_nickname(displayName[1])
        if not self.verify_signup(username,email,displayName,tel,date,password,verify,user_ob,user_ob1)[0]:
            unused,erroruser,errordisplay,errormail,errorpass,errorverify,errortel,errordesc,errordate = self.verify_signup(username,email,displayName,tel,date,password,verify,user_ob,user_ob1)
            date_pre = create_date()
            self.render('signup.html',pagename='Registrar',username=username[1],displayName=displayName[1],email=email[1],erroruser=erroruser,errormail=errormail,errorpass=errorpass,errorverify=errorverify,
                        errortel=errortel,errordisplay=errordisplay,errordate=errordate,errordesc=errordesc,tel=tel[1],description=description, years=date_pre[0],
                        months=date_pre[1],days=date_pre[2])
        else: #si el registro es valido
            user_ob = User(user_id=username[1],user_pw=hashlib.sha256(password[1]).hexdigest(),user_mail=email[1],
                            user_tel=tel[1],user_date=date,user_desc=description,user_type='user',solicitud_cambio=False, displayName=displayName[1],state=False,banned_from_comments=False,banned_from_posting=False) #se crea un objeto usuario con los datos
            user_ob.put() #se sube a la base de datos
            self.get_data('User','dict',user_ob.key().id(),user_ob,actualizar=True)
            self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.key().id())+'|'+hashlib.sha256(str(user_ob.key().id())).hexdigest()+';Path=/') #y se crea la cookie
            self.redirect('/profile')


#estas funciones sirven para validar el usuario,la contrasenia y el email, pero se le pueden agregar mas condiciones al verificar.
#Las salidas de dichas funciones son una tupla con un boolean como primer elemento y el usuario,contrasenia o email en el segundo
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if USER_RE.match(username):
        return (True,username)
    else:
        return (False,username)

DISPLAY_RE = re.compile(r"^[a-zA-Z0-9_ -]{3,20}$")
def valid_display(username):
    if DISPLAY_RE.match(username):
        return (True,username)
    else:
        return (False,username)

PASS_RE = re.compile(r"^[a-zA-Z0-9]{3,20}$")
def valid_pass(password):
    if PASS_RE.match(password):
        return (True,password)
    return (False,password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    if not email:
        return (False,'')
    if EMAIL_RE.match(email):
        return (True,email)
    return (False,email)

def valid_tel(tel):
    if not tel:
        return (False,tel)
    if tel.isdigit():
        if len(tel) > 7:
            return (True,tel)
    return (False,tel)

def valid_date(date):
    if not date:
        return (False,'')
    if date.isdigit():
        return (True,date)
    return (False,'')

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
