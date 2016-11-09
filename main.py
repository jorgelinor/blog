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
import admin
import test
import handler
import re
import search
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
    ('/profile/_viewcomments/?', profile.ViewComments),
    ("/profile/_sendpm/?", profile.SendPm),
    ("/([0-9]+)/?", permalink.Permalink),
    ('/([0-9]+)'+'/_editpost/?', permalink.EditPost),
    ('/([0-9]+)'+'/_editrequest/?', permalink.EditRequest),
    ("/admin/?", admin.Admin),
    ("/admin/([a-z0-9_-]+)", admin.Admin_submit),
    ("/admin/Admin_info", admin.Admin_info),
    ('/error/?', handler.ErrorHandler),
    ('/admin/stats', handler.Stats),
    ('/search', search.Search),
    ('/upload_photo', profile.PhotoUploadHandler),
    ('/view_photo/([^/]+)?', profile.ViewPhotoHandler)
], debug=True)
