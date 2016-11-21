import handler
from post import Post
import hashlib
from user import User
from comment import Comment
import time
from google.appengine.ext import db
from google.appengine.api import memcache

class Permalink(handler.Handler):
    #para ver la pagina de un post en particular
    def get(self,link,newcomment=False,editcomment=False,reportcomment=False,messages=None,com=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)#para la bandeja
        else:#si no 
            self.redirect('/login')#pal login
        post = self.get_data('Post')
        post = post.get(int(link))#obtiene el post
        if post:#si existe
            if self.request.get('action') == 'deletecomment':
                com = self.get_data('Comment')
                com = com.get(int(self.request.get('c')))# si el comentario existe con el query
                if com and int(com.post) == post.key().id() and post.submitter == user.user_id:
                    db.delete(com)
                    post.comments -= 1
                    post.put()
                    self.get_data('Post','dict',post.key().id(),post,actualizar=True)
                    self.get_data('Comment','dict',com.key().id(),None,actualizar=True)
                    time.sleep(1)
            if self.request.get("action") == "newcomment": #query para verificar si se agrega un nuevo comentario
                if not user.banned_from_comments:
                    newcomment = True# si es asi, manda algo al render para un espacio de comentario
                else:
                    self.redirect('/'+link)
            elif self.request.get('action') == 'editcomment':#query para editar un comentario
                com = self.get_data('Comment')
                com = com.get(int(self.request.get('c')))# si el comentario existe con el query
                if com and int(com.post) == post.key().id():#y tiene relacion con el post
                    editcomment = True#manda algo al render para editar
                else:#si no existe el comentario o no tiene relacion con el post
                    self.redirect("/error?e=comment-notfound")#se redirecciona a la pagina de error
            elif self.request.get('action') == 'reportcomment':
                com = self.get_data('Comment')
                com = com.get(int(self.request.get('c')))# si el comentario existe con el query
                if com and int(com.post) == post.key().id():#y tiene relacion con el post
                    reportcomment = True
                else:
                    self.redirect("/error?e=comment-notfound")#se redirecciona a la pagina de error
            post = self.display_names(user,[post])#camufla el usuario que lo envio
            comments = Comment.by_post(str(post[0].key().id()))#enlista los comentarios que tiene
            comments = self.display_names(user,comments)#camufla los usuarios de los comentarios
            self.render('permalink.html',pagename='Post',reportcomment=reportcomment,editcomment=editcomment,post=post[0],user=user,comments=comments,comment=com,recent_msg=messages,newcomment=newcomment)
        else:
            self.redirect("/error?e=post-notfound")#error
    def post(self,link):
        if self.request.get("action") == "newcomment":#para saber si la accion post o el metodo post es para nuevo comentario
            submitter = self.get_data('User')
            submitter = submitter.get(int(self.request.cookies.get('user_id').split('|')[0]))
            content = self.request.get("content")
            comments = self.get_data('Comment')#enlista los comentarios que tiene
            comments_list = self.to_list(comments,link)
            comments = self.display_names(submitter,comments_list)#camufla los usuarios de los comentarios
            post = self.get_data('Post')#obtiene el post
            post = post.get(int(link))
            if len(content) < 1:
                self.redirect('/'+link)
            else:
                com = Comment(submitter=submitter.user_id,content=content,post=link,reported=False,title="Comentario #"+str(len(list(comments))+1)+" en "+post.title,state=False)
                com.created_str = str(com.created)
                com.created_str = com.created_str[0:16]
                com.put()
                post.comments += 1
                post.put()
                self.get_data('Post','dict',int(link),post,actualizar=True)
                self.get_data('Comment','dict',com.key().id(),com,actualizar=True)
                self.redirect("/"+link)
        elif self.request.get('action') == 'editcomment':#para saber si la accion post o el metodo post es para editar un comentario
            content = self.request.get("content")
            if len(content) < 1:
                self.redirect("/"+link)
            else:
                com = Comment.get_by_id(int(self.request.get("c")))
                com.content = content
                com.created_str = str(com.created)
                com.created_str = com.created_str[0:16]
                com.put()
                self.get_data('Post','dict',int(link),Post.get_by_id(int(link)),actualizar=True)
                self.get_data('Comment','dict',com.key().id(),com,actualizar=True)
                self.redirect("/"+link)
        elif self.request.get('action') == 'reportcomment':
            razon = self.request.get("razon")
            if len(razon) < 1:
                self.redirect("/"+link)
            else:
                com = Comment.get_by_id(int(self.request.get("c")))
                com.razon = com.razon+[razon]
                com.reported = True
                com.put()
                self.get_data('Comment','dict',com.key().id(),com,actualizar=True)
                self.redirect("/"+link)

class EditPost(handler.Handler):
    def get(self,link,messages=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)#para la bandeja
        else:
            self.redirect("/login")
        post = Post.get_by_id(int(link))
        if post.submitter == user.user_id:#si el post pertenece al usuario
            if post.modificable == 'True':#y si es modificable se renderiza la edicion
                self.render('ascii.html',user=user,pagename='Editar post',title=post.title,post=post.post,error='',editable=True,recent_msg=messages)
            else:#si no es editable
                self.redirect("/"+str(post.key().id())+'/_editrequest')#se manda una peticion para editar
        else:#si el post no le pertenece al usuario
            self.redirect('/error?e=not-yourpost')#error

    def post(self,link):
        post = self.get_data('Post')
        post.get(int(link))
        content = self.request.get('content')
        if post and content:
            post.post = content
            post.modificable = "False"
            self.get_data('Post','dict',int(link),post,actualizar=True)
            post.put()
            self.redirect('/'+link)
        else:
            self.redirect('/'+link)

class EditRequest(handler.Handler):
    def get(self,link,messages=None):
        user = None
        if self.get_cookie_user(self.request.cookies.get('user_id'))[0]:
            user = self.get_data('User')
            user = user.get(int(self.request.cookies.get('user_id').split('|')[0]))
            messages = self.GetMessages(persona=user)#para la bandeja
        else:
            self.redirect("/login")
        post = self.get_data('Post')
        post = post.get(int(link))
        if post:#si hay post
            if post.submitter == user.user_id and post.modificable == 'False':#y si pertenece al usuario, y si no es modificable
                self.render('editrequest.html',user=user,pagename='Permiso para editar',post=post,recent_msg=messages)#se renderiza una peticion
            else:#de lo contrario
                self.redirect('/'+link)#pal post
        else:#si no existe el post
            self.redirect('/error?e=post-notfound')#error

    def post(self,link):
        razon = self.request.get('razon')
        if razon:
            post = self.get_data('Post')
            post = post.get(int(link))
            post.modificable = 'pending'
            post.razon = razon
            self.get_data('post_'+str(post.key().id()),post,actualizar=True)
            post.put()
        self.redirect('/'+link)
