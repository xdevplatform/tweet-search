$(document).ready(function(){

	$("#endpoints").hide();
	
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
	
	$(".tweet-save").click(function(){
		if ($(this).hasClass("btn-default")){
			$(this).removeClass("btn-default");
			$(this).addClass("btn-danger");
			$(this).html("Remove");
		} else {
			$(this).removeClass("btn-danger");
			$(this).addClass("btn-default");
			$(this).html("Save Tweet");
		}
		return false;
	})
	
	$("#generate_endpoints").click(function(){
		$("#endpoints").fadeIn();
		return false;
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

Graph = {
		
	init: function(lineData){
		
		var vis = d3.select('#visualisation'),
	    WIDTH = 800,
	    HEIGHT = 250,
	    MARGINS = {
	      top: 20,
	      right: 20,
	      bottom: 20,
	      left: 50
	    },
	    xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(lineData, function(d) {
	      return d.timePeriod;
	    }), d3.max(lineData, function(d) {
	      return d.timePeriod;
	    })]),
	    yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(lineData, function(d) {
	      return d.count;
	    }), d3.max(lineData, function(d) {
	      return d.count;
	    })]),
	    xAxis = d3.svg.axis()
	      .scale(xRange)
	      .tickSize(5)
	      .tickSubdivide(true),
	    yAxis = d3.svg.axis()
	      .scale(yRange)
	      .tickSize(5)
	      .orient('left')
	      .tickSubdivide(true);
	 
		vis.append('svg:g')
		  .attr('class', 'x axis')
		  .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
		  .call(xAxis);
		 
		vis.append('svg:g')
		  .attr('class', 'y axis')
		  .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
		  .call(yAxis);

		var lineFunc = d3.svg.line()
		  .x(function(d) {
		    return xRange(d.timePeriod);
		  })
		  .y(function(d) {
		    return yRange(d.count);
		  })
		  .interpolate('linear');
		
		vis.append('svg:path')
		  .attr('d', lineFunc(lineData))
		  .attr('stroke', 'blue')
		  .attr('stroke-width', 2)
		  .attr('fill', 'none');
		
	}	
	
}

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
