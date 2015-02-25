$(document).ready(function(){
	
	$("#activity_volume").hide();
	$("#activity_tweets").hide();

	$("#search").click(function(){
		
		$("#activity_volume").hide();
		$("#activity_tweets").hide();
		
		var query = $("#query").val();
		
		Page.loadChart(query);
		Page.loadTweets(query);
		

	});
		
});


var Page = {

	EMBED_TEMPLATE : '<article class="white-panel"><blockquote class="twitter-tweet" lang="en"><p>{{body}}</p>&mdash;{{actor.displayName}} ({{actor.preferredUsername}})<a href="{{object.link}}">{{object.postedTime}}</a></blockquote></article>',

	init : function() {

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
					
					tweets = response.tweets;
					for (var i = 0; i < tweets.length; i++){
						
						var tweet = tweets[i]
						var output = Mustache.render(Page.EMBED_TEMPLATE, tweet);
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
