$(document).ready(function() {
// By Default Disable radio button
    $(".well").find(':radio[name=topic]').attr('disabled', true);
    $('#topicos').find(':radio[name=topic]').css('opacity', '.2');
    $(".well").find(':radio[name=user]').attr('disabled', true);
    $('#users').find(':radio[name=user]').css('opacity', '.2');// This line is used to lightly hide label for disable radio buttons.
// Disable radio buttons function on Check Disable radio button.
});
$(':radio[value=topic]').click(function(event) {
    $(".well").find(':radio[name=user]').attr('disabled', true);
    $('#users').find(':radio[name=user]').css('opacity', '.3');
    $(".well").find(':radio[name=topic]').removeAttr('disabled');
    $('#topicos').find(':radio[name=topic]').css('opacity', '2');
    
});
$(':radio[value="user"]').click(function(event) {
    $(".well").find(':radio[name=topic]').attr('disabled', true);
    $('#topicos').find(':radio[name=topic]').css('opacity', '.3');
    $(".well").find(':radio[name=user]').removeAttr('disabled');
    $('#users').find(':radio[name=user]').css('opacity', '2');
});
$(":radio[name=topic]").click(function() {
    var value = $(this).val();
    $.ajax({

        url: '/admin/load',
        type: 'GET',
        dataType: 'json',
        data: {'topic': 'topic','topico':value},
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();

        $.each(data, function(index, el) {
            $('#contenido').append(
                    "<div name='"+el.post_id+"' id='"+el.post_id+"' class='col-md-8'>"
                    +"<a href='/admin/post_"+el.post_id+"'>someter informacion</a>"
                    +"<h4>post <a href="+el.title+">"+el.title+"</a></h4>"
                    +"<p>created:"+el.created+"</p>"
                    +"<h3>"+el.topic+"</h3>"
                    +"<b> creado: "+el.post+" </b>"
                    +"<b>"+el.razon+"</b><br>"
                    +"</div>");
        });
    }).fail(function() {
        $('#contenido').empty();
        $('#error').show();
        console.log("error");
    })
});

$(":radio[name=user]").click(function() {
    var value = $(this).val();
    $.ajax({
        url: '/admin/load',
        type: 'GET',
        dataType: 'json',
        data: {'topic':'user','user': value},
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        
        $.each(data, function(index, val) {
            $('#contenido').append("<div id='"+val.userid+"' name='"+val.userid+"' class='col-md-8'>"
                                        +"<p>Nombre de usurio:"+val.displayName+"</p>"
                                        +"<p>Usuario Estado:"+val.user_type+"</p>"
                                        +"<p>Rason de Cambio"+val.rason_solicitud_cambio+"</p>"
                                        +"<p>cambio de permiso para usuario </p>"
                                        +"<a href=/admin/user_"+val.userid+">someter informacion</a>"
                                        +"</div>");

        });
    }).fail(function() {
        $('#contenido').empty();
        $('#error').show();
        console.log("error");
    })
});

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
        if (!data) {
            $('#error').show();
        }
        $.each(data, function(index, el) {
            console.log('estado'+el.state);
            $('#contenido').append(
                    "<div name='"+el.comment_id+" class='col-md-8'>"
                    +"<a href='/admin/come_"+el.comment_id+"'>Someter informacion</a>"
                    +"<h3>coment submete by:"+el.submitter+"</h3>"
                    +"<b> creado: "+el.created+"</b><h4><a href="+el.post+">Post</a></h4>"
                    +"<h4>"+el.content+"</h4>"
                    +"<h5>Reportado</h5><b>"+el.razon+"</b><br name='query' value='comments_reported_cache'>"
                    +"</div>");

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
        if (!data) {
            $('#error').show();
        }
        $.each(data, function(index, el) {
            $('#contenido').append(
                    "<div name='"+el.post_id+"' id='"+el.post_id+"' class='col-md-8'>"
                    +"<a href='/admin/post_"+el.post_id+"'>someter informacion</a>"
                    +"<h4>post <a href="+el.title+">"+el.title+"</a></h4>"
                    +"<p>created:"+el.created+"</p>"
                    +"<h3>"+el.topic+"</h3>"
                    +"<b> creado: "+el.post+" </b>"
                    +"<b>"+el.razon+"</b><br>"
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
        data: { 'action': 'user_cache'}
    })
    .done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        if (!data) {
            $('#error').show();
        }
        $.each(data, function(index, val) {
            $('#contenido').append("<div id='"+val.userid+"' name='"+val.userid+"' class='col-md-8'>"
                                        +"<p>Nombre de usurio:"+val.displayName+"</p>"
                                        +"<p>Usuario Estado:"+val.user_type+"</p>"
                                        +"<p>Rason de Cambio"+val.rason_solicitud_cambio+"</p>"
                                        +"<p>cambio de permiso para usuario </p>"
                                        +"<a href=/admin/user_"+val.userid+">someter informacion</a>"
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

