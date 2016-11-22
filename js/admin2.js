
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
            $('#contenido').append(
                    "<div name='"+el.post_id+"' id='"+el.post_id+"' class='col-md-8'>"
                    +"<h4 class='page-header'>post <a href="+el.title+">"+el.title+"</a></h4>"
                    +"<p class='glyphicon glyphicon-time'>created:"+el.created+"</p>"
                    +"<h3>"+el.topic+"</h3>"
                    +"<b> "+el.post+" </b>"
                    +"<b>"+el.razon+"</b><br>"
                    +"<a href='/admin/post_"+el.post_id+"'>someter informacion</a>"
                    +"<hr></div>");
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
