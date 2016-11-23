


// informacion sometida por los usuarios
$("#asd").click(function() {
    console.log("asdfasdfsaf");
    $.ajax({
        url: '/admin/Admin_info',
        type: 'GET',
        dataType: 'json',
        data: { 'action': 'comments_cache'}
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        console.log(data);
        $.each(data, function(index, el) {
            
            console.log('estado'+el.state);
            $('#contenido').append(
                    "<div name='"+el.comment_id+"' class='col-md-8'>"
                    +"<h1 class='page-header'>Reporte enviado por: "+el.submitter+"</h1>"
                    +"<a href="+el.post+">"+el.title+"</a></h4>"
                    +"<p>"+el.content+"</p>"
                    +"<p>Razon:</p><b style='color:red'>"+el.razon+"</b><br name='query' value='comments_reported_cache'>"
                    +"<p class='glyphicon glyphicon-time'>"+el.created+"</p><br>"
                    +"<a href='/admin/come_"+el.comment_id+"'>Acciones de reporte</a>"
                    +"<hr></div>");

        });
    }).fail(function() {
        $('#error').show();
        console.log("'error'");
    });

});

$("#modificacion").click(function() {
    $.ajax({
        url: '/admin/Admin_info',
        type: 'GET',
        dataType: 'json',
        data: { 'action': 'post_cache'}
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        console.log(data);
        $.each(data, function(index, el) {
            $('#contenido').append(
                    "<div name='"+el.post_id+"' id='"+el.post_id+"' class='col-md-8'>"
                    +"<h4 class='page-header'>Pedido para <a href="+el.title+">este post</a> de "+el.topic+"</h4>"
                    +"<p class='glyphicon glyphicon-time'>"+el.created+"</p>"
                    +"<p>Razon para editar:</p>"
                    +"<b style='color:red'>"+el.razon+"</b><br>"
                    +"<a href='/admin/post_"+el.post_id+"'>Acciones de pedido</a>"
                    +"<hr></div>");
        });
    }).fail(function() {
        $('#contenido').empty();
        $('#error').show();
        console.log("error");
    });   
});
$("#administracion_user").click(function() {
    $.ajax({
        url: '/admin/Admin_info',
        type: 'GET',
        dataType: 'json',
        data: { 'action': 'user_cache'}
    })
    .done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        console.log(data);
        $.each(data, function(index, val) {
            $('#contenido').append("<div id='"+val.userid+"' name='"+val.userid+"' class='col-md-8'>"
                                        +"<p class='page-header'>Nombre de usurio:"+val.user_id+"</p>"
                                        +"<p>Tipo de permisos: "+val.user_type+"</p>"
                                        +"<p>Razon de cambio: "+val.rason_solicitud_cambio+"</p><br>"
                                        +"<a href=/admin/user_"+val.userid+">Modificar permisos de usuario</a>"
                                        +"<hr></div>");

        });
    })
    .fail(function() {
        $('#error').show();
        console.log("error");
    });
    
   
});

