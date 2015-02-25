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
					
					$("#total").html(response.total);
					$("#activity_volume").fadeIn();
														
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

						console.log(template);
						console.log(tweet);
						console.log(output);

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
