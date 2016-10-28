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
                "<ul id="+el.submitter+">"
                +"<h1>coment submete by:"+el.submitter+"</h1>"
                +"<b> creado: "+el.created+" </b><br><h4>post <a href="+el.post+">Post del mensaje</a></h4>"
                +"<div>"+el.content+"</div>"
                +"<h3>Reportado</h3><br><b>"+el.razon+"</b></ul>");
        });
    }).fail(function() {
        $('#error').show();
        console.log("error");
    });
    
});

$("#modificacion").click(function() {
    $.ajax({
        url: '/admin/Admin_info',
        type: 'GET',
        dataType: 'json',
        data: { 'action': 'post_modificable_cache'},
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        $.each(data, function(index, el) {
            $('#contenido').append("<ul id="+el.submitter+" >"
                +"<h4>post <a href="+el.title+">"+el.title+"</a></h4>"
                +"<h3>"+el.topic+"</h3>"
                +"<b> creado: "+el.post+" </b>"
                +"<br>"
                +"<h3 ><input>"+el.modificable+"</input></h3><br>"
                +"<b>"+el.razon+"</b></ul>");
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
        data: { 'action': 'user_permisos_cache'},
    })
    .done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        $.each(data, function(index, val) {
             $('#contenido').append('')
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