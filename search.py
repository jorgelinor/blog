from handler import Handler
from google.appengine.ext import db

class Search(Handler):
    def get(self,html=None,user=None,messages=None):        
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('user_'+self.request.cookies.get('user_id').split('|')[0],self.get_cookie_user(self.request.cookies.get('user_id'))[1])
            messages = self.GetMessages(actualizar=False,persona=user)#Los mensajes para mandarlos a la bandeja
        search = self.request.get('q')
        filter_search = self.request.get('filter')
        query = None
        if filter_search == 'User' or filter_search == 'Post' or filter_search == 'Comment':
            query = list(db.GqlQuery('select * from %s' % str(filter_search)))
        if query:
            html = []
            for ob in query:
                if filter_search == 'User':
                    if ob.displayName.lower().find(search.lower()) > -1:
                        html = html + [ob]
                elif filter_search == 'Post':
                    if ob.title.lower().find(search.lower()) > -1:
                        html = html + [ob]
                elif filter_search == 'Comment':
                    if ob.content.lower().find(search.lower()) > -1:
                        html = html + [ob]
        self.render('search.html',pagename='Resultados de busqueda',user=user,data=html,data_type=filter_search,recent_msg=messages,menu='filter',search=search)
