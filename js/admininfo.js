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
                "<div id='"+el.submitter+"'>"
                +"<h1>coment submete by:"+el.submitter+"</h1>"
                +"<b> creado: "+el.created+" </b><br><h4>post <a href="+el.post+">Post del mensaje</a></h4>"
                +"<div>"+el.content+"</div>"
                +"<h3>Reportado</h3><br><b>"+el.razon+"</b></div>"
                +"<input type='radio' name='report' value='True'>Quitar comentario</input>"+"<input type='radio' name='report' value='True'>Dejar comentratio</input>"
                +"<input type='submit' id='"+el.comment_id+"'></input>");
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
            $('#contenido').append("<div>"
                +"<h4>post <a href="+el.title+">"+el.title+"</a></h4>"
                +"<h3>"+el.topic+"</h3>"
                +"<b> creado: "+el.post+" </b>"
                +"<br>"
                +"<h3 ><input>"+el.modificable+"</input></h3><br>"
                +"<b>"+el.razon+"</b>"
                +"<input type='text' value='"+el.modificable+"'></imput>"
                +"<imput value='submit' id='"+el.post_id+"'></imput>"
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
        $.each(data, function(index, val) {
            $('#contenido').append("<div>"
                                    +"<p>Nombre de usurio:"+val.displayName+"</p>"
                                    +"<p>Usuario Estado:"+val.user_type+"</p>"
                                    +"<p>Rason de Cambio"+val.rason_solicitud_cambio+"</p>"
                                    +"<p>cambio de permiso para usuario </p>"
                                    +"<input type='text' id='"+val.user_id+"' ></input>"
                                    +"<input type='submit,';></input>"
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
    
   
// });
    // "<div id="+el.user_id+">"
    //     +"<p>Nombre de usurio:"+le.displayName+"</p>"
    //     +"<p>Usuario Estado:"+le.user_type+"</p>"
    //     +"<p>Rason de Cambio"+le.rason_solicitud_cambio+"</p>"
    //     +"<p>cambio de permiso para usuario </p>"
    //     +"<input type='text'id='"le.user_id"' value=''></input>"
    //     +"<input></input>"
    // +"</div>"
    