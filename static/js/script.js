$(document).ready(function(){

	$(".term").click(function(){
		var query = $("#query").val();
		var val = $(this).val();
		var newTerm = " OR (" + val + ")";
		var finalTerm = ""
		if ($(this).is(':checked')){
			if (query.indexOf("OR") < 0){
				query = "(" + query + ")"
			}
			finalTerm = query + newTerm
		} else {
			if (query.indexOf(newTerm) >= 0){
				finalTerm = query.replace(newTerm, "");
			}
		}
		$("#query").val(finalTerm);
	});

});