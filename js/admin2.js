
// By Default Disable radio button
$(".well").find(':radio[name=topic]').attr('disabled', true);
$('#topicos').find(':radio[name=topic]').css('opacity', '.2');
$(".well").find(':radio[name=user]').attr('disabled', true);
$('#users').find(':radio[name=user]').css('opacity', '.2');// This line is used to lightly hide label for disable radio buttons.
// Disable radio buttons function on Check Disable radio button.
// 
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
    var topic = $(this).val();
    console.log(topic);
    $.ajax({
        url: '/admin_topic',
        type: 'GET',
        dataType: 'json',
        data: {'topico':topic},
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        console.log(data);
        $.each(data, function(index, el) {
            if (el.modificable != 'pending'){
                var editable = (el.modificable) ? 'Sí':'No'
                $('#contenido').append(
                    "<div name='"+el.post_id+"' id='"+el.post_id+"' class='col-md-8'>"
                    +"<h4 class='page-header'><a class='admin-link' style='color:black' href="+el.post_id+">"+el.title+"</a></h4>"
                    +"<p>Dueño de este post: " + el.submitter + "</p>"
                    +"<p>Este post es editable: "+ editable + "</p>"
                    +"<p>Tópico: "+el.topic+"</p>"
                    +"<p class='glyphicon glyphicon-time'>"+el.created+"</p><br>"
                    +"<a class='admin-link' style='color:black' href='/admin/post2_"+el.post_id+"'>Acciones de post</a>"
                    +"<hr></div>");    
            }
            
        });
    }).fail(function() {
        $('#contenido').empty();
        $('#error').show();
        console.log("error");
    });
       
});

$(":radio[name=user]").click(function() {
    var value = $(this).val();
    $.ajax({
        url: '/admin_load',
        type: 'GET',
        dataType: 'json',
        data: {'user': value}
    }).done(function(data) {
        $('#contenido').empty();
        $('#error').hide();
        $.each(data, function(index, val) {
            var posts_perm = (val.banned_from_posting) ? 'No':'Si' 
            var comments_perm = (val.banned_from_comments) ? 'No':'Si' 
            var type = (val.user_type == "admin") ? 'Administrador':'Usuario'
            $('#contenido').append("<div id='"+val.userid+"' name='"+val.userid+"' class='col-md-8'>"
                                        +"<h3 class='page-header'>"+val.user_id+"</h3>"
                                        +"<p>Apodo: "+val.displayName+"</p>"
                                        +"<p>Permisos de usuario: "+type+"</p>"
                                        +"<p>Permisos para postear: "+posts_perm+"</p>"
                                        +"<p>Permisos para comentar: "+comments_perm+"</p>"
                                        +"<a href=/admin/user_"+val.userid+">Modificar permisos de usuario</a>"
                                        +"</div>");

        });
    }).fail(function() {
        $('#contenido').empty();
        $('#error').show();
        console.log("error");
    })
});
