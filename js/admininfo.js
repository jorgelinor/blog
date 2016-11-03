$("#asd").click(function() {
    console.log("asdfasdfsaf");
    $.ajax({
        url: '/admin/Admin_info',
        type: 'GET',
        dataType: 'json',
        data: { 'action': 'comments_reported_cache'}
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        $.each(data, function(index, el) {
            
            $('#contenido').append(
                "<div id='"+el.comment_id+"'style=''>"
                    +"<h1>coment submete by:"+el.submitter+"</h1>"
                    +"<b> creado: "+el.created+" </b><br><h4>post <a href="+el.post+">Post del mensaje</a></h4>"
                +"<div>"+el.content+"</div>"
                +"<h3>Reportado</h3><br><b>"+el.razon+"</b>"
                +"<input type='checkbox' name='report'>Quitar comentario</input><br>"
                +"<button class='submit'>enviar</button></div>");
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
        data: { 'action': 'post_modificable_cache'}
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        $.each(data, function(index, el) {
            console.log(el.submitter);
            $('#contenido').append("<div id='"+el.post_id+"' style=''>"
                +"<h4>post <a href="+el.title+">"+el.title+"</a></h4>"
                +"<h3>"+el.topic+"</h3>"
                +"<b> creado: "+el.post+" </b>"
                +"<br>"
                +"<h3 ><input>"+el.modificable+"</input></h3><br>"
                +"<b>"+el.razon+"</b>"
                +"<input type='text' value='"+el.modificable+"'></input>"
                +"<button class='submit'></button>"
                +"</div>");
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
        data: { 'action': 'user_permisos_cache'}
    })
    .done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        var cuenta = -1
        $.each(data, function(index, val) {
            cuenta = cuenta + 1; 
            $('#contenido').append("<div id='"+val.userid+"' style=''>"
                                    +"<p>Nombre de usurio:"+val.displayName+"</p>"
                                    +"<p>Usuario Estado:"+val.user_type+"</p>"
                                    +"<p>Rason de Cambio"+val.rason_solicitud_cambio+"</p>"
                                    +"<p>cambio de permiso para usuario </p>"
                                    +"<input type='text'></input>"
                                    +"<buton type='submit' class='submit'></button>"
                                    +"</div>");
        });
    })
    .fail(function() {
        $('#error').show();
        console.log("error");
    });
    
   
});
// $("#administracion_post").click(function() {
//     $.ajax({
//         url: '/admin/Admin_info',
//         type: 'GET',
//         dataType: 'json',
//         data: { 'action': 'user_permisos_cache'},
//     })
//     .done(function(data) {
//         console.log(data);
//     })
//     .fail(function() {
//         console.log("error");
//     })
//     .always(function() {
//         console.log("complete");
//     });
    
$(".submit").click(function(){
    var id = $(this).parent().attr("id");
    var estado = $(this).siblings('input').prop('checked');
    $.ajax({
        type     : "POST",
        url      : '/admin/Admin_info',
        dataType : "json",
        data : {"query":'comments_reported_cache' ,"id": id, "estado":estado}
    }).success( function(data) {
            if(data == 'True'){ 
                // $(this).css("border": "#00ff00");
                $(this).parent().css({'display':'none'});
            };
        });

});

$(".submit").click(function(){
    var id = $(this).parent().attr("id");
    var estado = $(this).siblings('input').prop('text');
    $.ajax({
        type     : "POST",
        url      : '/admin/Admin_info',
        dataType : "json",
        data : {"query":'post_modificable_cache' ,"id": id, "estado":estado}
    }).success( function(data) {
            if(data == 'True'){ 
                // $(this).css("border": "#00ff00");
                $(this).parent().css({'display':'none'});
            };
        });
});    