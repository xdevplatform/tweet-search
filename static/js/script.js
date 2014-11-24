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


	var client = new ZeroClipboard($(".copy-button"));

	client.on( "ready", function( readyEvent ) {
		  // alert( "ZeroClipboard SWF is ready!" );

		  client.on( "aftercopy", function( event ) {
		    // `this` === `client`
		    // `event.target` === the element that was clicked
		    // event.target.style.display = "none";
			  
			$(event.target).tooltip('show');
			  
			// alert("Copied text to clipboard: " + event.data["text/plain"] );
		  } );
		} );
	
	Utils.clipboardSetData();
});

Utils = {

    init: function(){
        this.counter = 1;
    },
    
    clipboardSetData: function(){
    	$(".copy-button").each(function (){
    		var el = $(this);
    		var pre = el.parent().siblings("pre");
    		// var clipboardText = pre.attr("data-clipboard-text");
    		// if (!clipboardText){
			var clipboardText = Utils.htmlDecode(pre.html());
    		// }
    		if (clipboardText){
    			el.attr("data-clipboard-text", clipboardText);
    			// alert(el.attr("data-clipboard-text"))
    		}
    	});
    },
    
	qs: function(obj) {
      var str = [];
      for(var p in obj){
         str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
      return str.join("&");
    },
    
    htmlEncode: function(textContent){
    	return $("<textarea/>").text(textContent).html();
    },

    htmlDecode: function(textContent){
    	return $("<textarea/>").html(textContent).text();
    }

}
