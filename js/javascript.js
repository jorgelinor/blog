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
