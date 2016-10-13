import webapp2
import os
import sys
import newpost
import login
import signup
import logout
import page
import profile
import permalink

#este es el archivo principal, si se crea una pagina o archivo nuevo se debe importar aqui y asignarle un path de referencia



app = webapp2.WSGIApplication([
    ('/newpost', newpost.Newpost),
    ('/signup',signup.Signup),
    ('/login',login.Login),
    ('/logout',logout.Logout),
    ('/',page.Page),
    ('/profile/?', profile.Profile),
    ('/profile/_edit/?', profile.EditProfile),
    ('/profile/_editpass/?',profile.EditPass),
    ('/profile/_viewposts/?', profile.ViewPosts),
    #('/profile/_viewcomments/?', profile.ViewComments),
    ("/([0-9]+)/?", permalink.Permalink),
    ("/([0-9]+)"+"/_reply", permalink.Comment),
], debug=True)
