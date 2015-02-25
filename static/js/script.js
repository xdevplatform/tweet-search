$(document).ready(function(){
	
	Page.init();


		
});


var Page = {

	init : function() {

		Page.clear();
		$('#buffer').collapse('show');
		
		$('#query').bind("propertychange change click keyup input paste", function (e) {
			
			  if (e.which == 13) {
				  $("#search").click();
			  }
			  
			  var query = $("#query").val();
			  if (!query || query == ''){
				  Page.clear();
				  $('#buffer').collapse('show');
			  }
			  
			});
		
		$("#search").click(function(){

			var query = $("#query").val();
			if (query){
				
				Page.clear();
				$('#buffer').collapse('hide');
				Page.loadChart(query);
				Page.loadTweets(query);
			}
			
		});
		
		$(document.body).on('click', '.term', function(){
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
		
	},
	
	clear : function(){
		$("#activity_volume").hide();
		$("#activity_tweets").hide();
		$("#tweets").html("");
	},

	loadChart : function(query) {

		 $.ajax({
				type : "GET",
				url : "/query/chart",
				data : {"query" : query},
				dataType : "json",
				success : function(response) {
					
					console.log(response);
					
					var args = {
						    bindto: '#chart',
						    data: {
						        x: 'x',
						        // xFormat: '%Y%m%d', // 'xFormat' can be used as custom format of 'x'
						        columns: response.columns
						    },
						    axis: {
						        x: {
						            type: 'timeseries',
						            tick: {
						                format: '%Y-%m-%d'
						            }
						        }
						    }
						};
					var chart = c3.generate(args);
					
					$("#total").html(Utils.integerFormat(response.total));
					$("#activity_volume").fadeIn();
					
					template = $("#templateFrequency").html();
					Mustache.parse(template);
					
					var frequency = response.frequency;
					for (var i = 0; i < frequency.length; i++){
						
						var f = frequency[i];
						f.mentionPercent = function(){
							return Math.round(this[1] * 100) + "%" 
						}
						f.activityPercent = function(){
							return Math.round(this[3] * 100) + "%" 
						}
						
						
						var output = Mustache.render(template, f);
						$("#frequency").append(output);

					}
														
				},
				error : function(xhr, errorType, exception) {
					console.log('Error occured');
				}
			});
	
	},
	
	loadTweets : function(query) {
		
		 $.ajax({
				type : "GET",
				url : "/query/tweets",
				data : {"query" : query},
				dataType : "json",
				success : function(response) {
					
					console.log(response);
					
					template = $("#templateTweet").html();
					Mustache.parse(template);
					
					tweets = response.tweets;
					for (var i = 0; i < tweets.length; i++){
						
						var tweet = tweets[i];
						
						var output = Mustache.render(template, tweet);
						$("#tweets").append(output);

					}
					
					window.twttr.widgets.load()
					
					$("#activity_tweets").fadeIn();
														
				},
				error : function(xhr, errorType, exception) {
					console.log('Error occured');
				}
			});
		 
	},
	
}

Utils = {

	integerFormat : function(x) {
		    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
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
