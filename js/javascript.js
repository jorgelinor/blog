function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.img-viewer-img').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#imginput").change(function(){
    readURL(this);
});

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
function setCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function getCookie(name){
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
    createCookie(name,"",-1);
}
function load_data(posts,mios,request,limit) {
	if (getCookie("limit")!=null){
		if (mios=="True"){
			var limit = parseInt(getCookie("limit").split("|")[0])
		}
	}
	lim = limit
	$(".page-content").empty();
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
			$('.page-content').append("<br><hr>")
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
			$('.page-content').append("<br><hr>")
		}
	}
	if (getCookie("limit") != null){
		if (mios=="True"){
			$(window).scrollTop(parseInt(getCookie("limit").split("|")[1]))
		}
	}
	$(window).scroll(function() {
		if (mios=="True") {
			setCookie('limit',limit+"|"+$(window).scrollTop())
		}
		if($(window).scrollTop() == $(document).height() - $(window).height()) {
		    if (posts.length > lim){
			    lim = limit + 5
			    setCookie('limit',lim+"|"+$(window).scrollTop())
			    $("#loading").empty()
				$("#loading").append("<img src='http://i.stack.imgur.com/h6viz.gif' alt='loading'></img>")
			    setTimeout(function(){
			 	 	load_data(posts=posts,mios=mios,request=request,limit=lim)
			 	 	$("#loading").empty()
			    },2000)
		    }
	    }
	})
}
function lol(){
	console.log('hola')
}

$('.img').click(function(){
	$('.img-viewer').css("display","block")
})
$('.img').hover(function(){
	$('#hover-view').css('opacity','0.3')
},function(){
	$('#hover-view').css('opacity','0')
})
$('#img-viewer-close').click(function(){
	$('.img-viewer').css('display','none')
})

$('.people-container').hover(function(){
	$(this).css('background-color','#ffff66')
},function(){
	$(this).css('background-color','#ffffff')
})

