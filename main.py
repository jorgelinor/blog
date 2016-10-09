import webapp2
import os
import sys
import newpost
import login
import signup
import logout
import page

#este es el archivo principal, si se crea una pagina o archivo nuevo se debe importar aqui y asignarle un path de referencia



app = webapp2.WSGIApplication([
    ('/newpost', newpost.Newpost),('/signup',signup.Signup),('/login',login.Login),('/logout',logout.Logout),('/',page.Page)
], debug=True)
