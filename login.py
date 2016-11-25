#Clase de inicio de sesion
# -*- coding: utf-8 -*-
import handler
import hashlib
from user import User
import re
from google.appengine.ext import db

class Login(handler.Handler):
    def get(self):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            self.redirect("/error?e=already-logged")
        else:
            self.render('login.html',pagename='Iniciar sesion',url='Login',link='/')

    def post(self):
        username = valid_username(self.request.get('username'))
        password = valid_pass(self.request.get('password'))
        user_query = User.by_username(self.request.get('username')) #<---esta variable la uso mucho a la hora de asignar un objeto usuario
        if not self.verify_login(username,password,user_query)[0]:
            unused,errorpass,erroruser = self.verify_login(username,password,user_query)
            self.render('login.html',pagename=u'Iniciar sesión',username=username[1],erroruser=erroruser,errorpass=errorpass)
        else: #si todo esta correcto
            self.response.headers.add_header('Set-Cookie','user_id='+str(user_query.key().id())+'|'+hashlib.sha256(str(user_query.key().id())).hexdigest()+';Path=/') #se hace la cookie del usuario
            self.redirect('/profile')

#estas funciones sirven para validar el usuario y la contrasenia, pero se le pueden agregar mas condiciones al verificar.
#Las salidas de dichas funciones son una tupla con un boolean como primer elemento y el usuario o contrasenia en el segundo
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
