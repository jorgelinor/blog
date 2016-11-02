from handler import Handler
from google.appengine.ext import db

class Search(Handler):
	def get(self):
		html = '<h1>Resultados de busqueda</h1>'
		search = self.request.get('u')
		query = list(db.GqlQuery('select * from User'))
		for user in query:
			if user.displayName.lower().find(search.lower()) > -1:
				html = html + "<a href='/profile?u="+user.displayName+"'><div>"+user.displayName+'</div>'+'</a>'
		self.write(html)