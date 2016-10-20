#Clase de registro
import random
import string
import handler
from user import User
import hashlib
import re
from google.appengine.ext import db

class Signup(handler.Handler):
    def get(self):
        user = None
        date_pre = self.get_data('create_date',create_date())
        if not self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            self.render('signup.html',pagename='Registrar',url='Signup',link='/',years=list(reversed(date_pre[0])),months=date_pre[1],days=date_pre[2])
        else:
            self.write("<a href='/'>Already registered</a>")
        
    def post(self):
        randomStr = ''.join(random.choice(string.letters) for _ in xrange(5))
        username = valid_username(self.request.get('username'))
        password = valid_pass(self.request.get('password'))
        tel = valid_tel(self.request.get('tel'))
        date = valid_date(self.request.get('date1'))[1]+'-'+valid_date(self.request.get('date2'))[1]+'-'+valid_date(self.request.get('date3'))[1]
        description = self.request.get('description')
        verify = self.request.get('verify')==self.request.get('password')
        email = valid_email(self.request.get('email'))
        erroruser,errormail,errorpass,errorverify,errortel,errordesc,errordate='','','','','','',''
        user_query = db.GqlQuery('select * from User where user_id=:1',username[1])
        user_query = list(user_query)
        user_ob = None #<---esta variable la uso mucho a la hora de asignar un objeto usuario
        if user_query:
            user_ob = user_query[0]
        if not(username[0] and tel[0] and len(date)>7 and email and password[0] and verify and email[0] and not user_ob):
            if not username[0]:
                erroruser = 'Invalid username'
            if user_ob:
                erroruser = 'Username already exists'
            if not password[0]:
                errorpass = 'Invalid password'
            if not verify:
                errorverify = "Passwords don't match"
            if not tel[0]:
                errortel = 'Introduce a phone number'
            if not len(date)>7:
                errordate = 'Invalid Birth Date'
            if not email[0]:
                errormail = 'Invalid e-mail'
            date_pre = create_date()
            self.render('signup.html',pagename='Registrar',username=username[1],email=email[1],erroruser=erroruser,errormail=errormail,errorpass=errorpass,errorverify=errorverify,
                        errortel=errortel,errordate=errordate,errordesc=errordesc,tel=tel[1],description=description,years=list(reversed(date_pre[0])),
                        months=date_pre[1],days=date_pre[2])
        else: #si el registro es valido
            user_ob = User(user_id=username[1],user_pw=hashlib.sha256(password[1]).hexdigest(),user_mail=email[1],
                            user_tel=tel[1],user_date=date,user_desc=description,user_type='user',displayName=username[1]+randomStr) #se crea un objeto usuario con los datos
            user_ob.put() #se sube a la base de datos
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
    years,months,days = [],[],[]
    for e in range(1,32):
        days.append(e)
    for e in range(1,13):
        months.append(e)
    for e in range(1950,2013):
        years.append(e)
    return (years,months,days)
