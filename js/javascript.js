var activate = function() {
	$("#bandeja").css("display","block");
	$("#bandeja").css("background-color","gray");
	$("#inbox-link").attr("onclick","deactivate()")

}

var deactivate = function() {
	$("#bandeja").css("display","none")
	$("#bandeja").css("background-color", "none")
	$("#inbox-link").attr("onclick","activate()")
}

function load_data(posts,mios,request,limit) {
	lim = limit
	$(".page-content").empty();
	$('.page-content').append('<br><br><br><br>')
	for (post in posts.slice(0,limit)) {
		if (posts[post].visible == false){
			if (mios=="True") {
				$(".page-content").append('<center><h2 style="margin-left:20%;margin-right:20%;margin-bottom:70px"><a id="post-title" style="color:red" href="/'+posts[post].id+'">'+posts[post].title+'</a></h2><a href="/profile/_viewposts?post='+posts[post].id+'&visible=1"><button id="edit-link">Mostrar</button></a><div style="max-width:500px;word-wrap:break-word"><pre>'+posts[post].post+'</pre></div>')
				if (posts[post].submitter.split("|")[1] != "False") {
					$(".page-content").append('<label style="float:left">Enviado por: <a id="post-submitter" href="/profile?u='+posts[post].submitter.split("|")[0]+'">'+posts[post].submitter.split("|")[0]+'</a></label>')
				} else {
					$(".page-content").append('<label style="float:left">Enviado por: <a id="post-submitter-deleted">'+posts[post].submitter.split("|")[0]+'</a></label>')
				}
				$(".page-content").append('<label style="float:right">'+posts[post].created_str+'</label><label style="float:right;color:gray;font-style:italic">')
				if (posts[post].comments > 1) {
					$(".page-content").append('<label style="float:right;color:gray;font-style:italic">'+posts[post].comments+' comentarios&nbsp;&nbsp;</label>')
				} else {
					if (posts[post].comments == 1) {
						$(".page-content").append('<label style="float:right;color:gray;font-style:italic">'+'1 comentario&nbsp;&nbsp;</label>')
					}
				}
				if (request) {
					$(".page-content").append('Razon: <label class="reported-comment" style="color:red;">'+posts[post].razon+'</label><a href="/admin/post_requests?post='+posts[post].id+'&action=deny_request"><button id="edit-link">Rechazar</button></a><a href="/admin/post_requests?post='+posts[post].id+'&action=accept_request"><button id="edit-link">Permitir</button></a>')
				}
				
			}
		} else {
			$(".page-content").append('<center><h2 style="margin-left:20%;margin-right:20%;margin-bottom:70px"><a id="post-title" href="/'+posts[post].id+'">'+posts[post].title+'</a></h2>')
			if (mios=="True") {
				$(".page-content").append('<a href="/profile/_viewposts?post='+posts[post].id+'&visible=0"><button id="edit-link">Ocultar</button></a>')
			}
			$('.page-content').append('<center><div style="max-width:500px;word-wrap:break-word"><pre>'+posts[post].post+'</pre></div></center>')
			if (posts[post].submitter.split("|")[1] != "False") {
				$('.page-content').append('<label style="float:left">Enviado por: <a id="post-submitter" href="/profile?u='+posts[post].submitter.split('|')[0]+'">'+posts[post].submitter.split("|")[0]+'</a></label>')
			} else {
				$('.page-content').append('<label style="float:left">Enviado por: <a id="post-submitter-deleted">'+posts[post].submitter.split("|")[0]+'</a></label>')
			}
			$('.page-content').append('<label style="float:right">'+posts[post].created_str+'</label>')
			if (posts[post].comments > 1) {
				$(".page-content").append('<label style="float:right;color:gray;font-style:italic">'+posts[post].comments+' comentarios&nbsp;&nbsp;</label>')
			} else {
				if (posts[post].comments == 1) {
					$(".page-content").append('<label style="float:right;color:gray;font-style:italic">'+'1 comentario&nbsp;&nbsp;</label>')
				}
			}
			if (request) {
				$(".page-content").append('Razon: <label class="reported-comment" style="color:red;">'+posts[post].razon+'</label><a href="/admin/post_requests?post='+posts[post].id+'&action=deny_request"><button id="edit-link">Rechazar</button></a><a href="/admin/post_requests?post='+posts[post].id+'&action=accept_request"><button id="edit-link">Permitir</button></a>')
			}
		}
		if (posts[post].visible == true){
			$('.page-content').append("<br><hr>")
		} else {
			if (posts[post].visible == false) {
				if (mios=="True"){
					$('.page-content').append("<br><hr>")
				}
			}
		}
	}
	$(window).scroll(function() {
		if($(window).scrollTop() == $(document).height() - $(window).height()) {
		    if (posts.length > lim){
			    lim = limit + 5
			    setTimeout(function(){
			 	 	load_data(posts=posts,mios=mios,request=request,limit=lim)
			    },2000)
		    }
	    }
	})
}
