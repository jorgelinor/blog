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
    def GetMessages(self,actualizar,persona):
    	messages = memcache.get(persona)
    	if actualizar == True or messages == None:
    		messages = db.GqlQuery("select * from Message where destination='"+persona+"' order by date desc")
    		memcache.set(persona,messages)
    		messages = list(messages)
    		for e in messages:
    			if e.submitter != "Administracion":
    				e.submitter = db.GqlQuery("select * from User where user_id='"+e.submitter+"'").fetch(1)[0].displayName
    	return list(messages)
    def get_data(self,key,query):
        data = memcache.get(key)
        if data is not None:
            return data
        else:
            data = query
            self.write('algo')
            memcache.add(key, data)
        return data
    def delete_data(self,key):
    	memcache.delete(key)
    def get_cookie_user(self,cookie):
    	if cookie:
    		if cookie.split("|")[0].isdigit():
    			if hashlib.sha256(cookie.split("|")[0]).hexdigest() == cookie.split("|")[1]:
    				if User.get_by_id(int(cookie.split("|")[0])):
    					return (True,User.get_by_id(int(cookie.split("|")[0])))
    	return (False,None)
