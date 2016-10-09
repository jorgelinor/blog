from google.appengine.api import memcache
import re
import random
import string
from xml.dom import minidom
import urllib2
import logging
import imp
import webapp2
import os
import sys
import newpost
import login
import signup
import logout
import page





app = webapp2.WSGIApplication([
    ('/newpost', newpost.Newpost),('/signup',signup.Signup),('/login',login.Login),('/logout',logout.Logout),('/',page.Page)
], debug=True)
