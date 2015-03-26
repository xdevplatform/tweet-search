$(document).ready(function(){
	
	Page.init();
		
});


var Page = {
		
	maxQueries : 4,

	init : function() {

		$("#chart_loading").hide();
		$("#tweets_loading").hide();
		
		$('.datetimepicker').datetimepicker({
	    	format: 'YYYY-MM-DD HH:mm',
	    	pickTime: true
		});
		
		Page.clear();
		$('#buffer').collapse('show');

		$(".query-input").on("keydown", function (e) {

			// on TAB, add query input 
			if (e.which == 9) {
				  Page.queryAdd();
				  console.log(".query-input keydown" + e.which);
			}

			return true;
		});
		
		$(".query-input").on("keyup", function (e) {
			
			  // on ENTER, search
			  if (e.which == 13) {
				  Page.search();
			  }
			  
			  var query = $("#query0").val();
			  if (!query || query == ''){
				  Page.clear();
				  $('#buffer').collapse('show');
			  }
			  
			  console.log(".query-input keyup" + e.which);
			  
			  return true;
			  
			});
		
		$(".query-add").hide();
		
		$("#queryAdd").on("click", function(){
			
			Page.queryAdd();
		});
		
		$(".queryRemove").on("click", function(){
			
			Page.queryRemove(this);

		});
		
		$("#scrolltop").on("click", function(){

			window.scrollTo(0, 0);
			return false;
			
		});
		
		$("#search").on("click", function(){

			Page.search();
			
		});
		
		$('#media').on("click", function(){
			Page.toggleTerm("(has:media)", $(this).is(':checked'));
		});
		
		$("#retweet_help").hide();
		$('#retweet').on("click", function(){
			Page.toggleTerm("(is:retweet)", $(this).is(':checked'));
			if ($(this).is(':checked')){
				$("#retweet_help").fadeIn();
			} else {
				$("#retweet_help").fadeOut();
			}
		});
		
		$(document).on("click", ".term", function(){
			var val = $(this).val();
			var newTerm = "(" + val + ")";
			Page.toggleTerm(newTerm, $(this).is(':checked'));
		});
		
	},
	
	toggleTerm : function(term, checked){
		$(".query-input").each(function(){
			var query = $(this).val();
			var newTerm = " " + term;
			var finalTerm = ""
			if (checked){
				finalTerm = query + newTerm
			} else {
				if (query.indexOf(newTerm) >= 0){
					finalTerm = query.replace(newTerm, "");
				}
			}
			$(this).val(finalTerm);
		});
	},
	
	clear : function(){
		$("#activity_volume").hide();
		$("#activity_tweets").hide();
		$("#chart").html("");
		$("#tweets").html("");
	},
	
	queryAdd : function(){
		for (var i = 1; i < Page.maxQueries; i++){
			var id = "#query" + i + "_holder";  
			if ($(id).is(':hidden')){
				$(id).fadeIn();
				break;
			}
		}
	},
	
	queryRemove : function(element){
		var id = $(element).data("id");
		var id = "#" + id;
		$(id).hide();
		$(id).find("input").val("");
	},
	
	search : function(){
		var singleQuery = true;
		var query0 = $("#query0").val();
		if (query0){
			
			var now = "";
			var start = $("#start").val();
			var end = $("#end").val();
			var embedCount = $("#embedCount").val();
			
			Page.clear();
			$('#buffer').collapse('hide');
			
			var queries = [query0];
			for (var i = 1; i < Page.maxQueries; i++){
				var query = $("#query" + i).val();
				if (query){
					queries.push(query);
					singleQuery = false;
				}
			}
			
			if ($("#results_chart").is(':checked')){
				Page.loadChart(queries, start, end);
			}
			
			if (singleQuery){

				Page.loadFrequency(query0, start, end);

				if ($("#results_tweets").is(':checked')){
					Page.loadTweets(query0, start, end, embedCount);
				}

				if ($("#results_export").is(':checked')){
					Page.loadExport(query0, start, end, embedCount);
				}
			} else {
				
			}
}
	},

	loadChart : function(queries, start, end) {

		 $("#chart_loading").show();

	 	 var data = {"start": start, "end": end};
	 	 if (queries.length == 1){
	 		 data["query"] = queries[0]; 
	 	 } else {
	 		data["queries"] = queries;
	 	 }
		 
		 $.ajax({
				type : "GET",
				url : "/query/chart",
				data : data,
				dataType : "json",
				success : function(response) {
					
					// console.log(response);
					var start = response.start;
					
					var args = {
						    bindto: '#chart',
						    point: {
					    	  show: false
					    	},
					    	interaction: {
				    		  enabled: false
				    		},
						    data: {
						    	labels: false,
//						        x: 'x',
//						        xFormat: '%Y-%m-%d', // 'xFormat' can be used as custom format of 'x'
						        columns: response.columns,
							    colors: {
						            count: '#4099FF'
						        }
						    },
						    axis: {
						        x: {
//						            type: 'timeseries',
						            tick: {
						            	culling: true,
						            	count: response.days + 1,
						            	format: function (x) {
						            		var days = x / 24;

						            		var date = new Date(start.valueOf());
						            	    date.setDate(date.getDate() + days);

						            	    var dateStr = (date.getMonth() + 1) + '/' + date.getDate() + '/' +  date.getFullYear()
//					            			console.log(dateStr);
					            			return dateStr;
				            			}
//						                format: '%Y-%m-%d'
						            }
						        }
						    }
						};
					
					console.log(args);
					var chart = c3.generate(args);
					
					$("#total").html(Utils.integerFormat(response.total));
					$("#activity_volume").fadeIn();
					$("#chart_loading").hide();
					
				},
				error : function(xhr, errorType, exception) {
					console.log('Error occured');
				}
			});
	
	},

	loadFrequency : function(query, start, end) {

	 	var data = {"start": start, "end": end, "query": query};
	 	 
	 	console.log(data);
		 
		$("#frequency").find("tr:gt(0)").remove();

		templateLoading = $("#templateFrequencyLoading").html();
		$("#frequency").append(templateLoading);
			
		 $.ajax({
				type : "GET",
				url : "/query/frequency",
				data : data,
				dataType : "json",
				success : function(response) {
					
					$("#frequency").find("tr:gt(0)").remove();
					
					var frequency = response.frequency;
					console.log(frequency)
					if (frequency){
						
						template = $("#templateFrequency").html();
						Mustache.parse(template);
						
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
					}
					
				},
				error : function(xhr, errorType, exception) {
					console.log('Error occured');
				}
			});
	
	},
	
	loadTweets : function(query, start, end, embedCount) {
		
		 $("#tweets_loading").show();
		
		 $.ajax({
				type : "GET",
				url : "/query/tweets",
				data : {"query" : query, "start": start, "end": end, "embedCount": embedCount},
				dataType : "json",
				success : function(response) {
					
//					console.log(response);
					
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
					
					$("#tweets_loading").hide();
														
				},
				error : function(xhr, errorType, exception) {
					console.log('Error occured');
				}
			});
		 
	},
	
	loadExport : function(query, start, end, embedCount) {
		
		data = {"query" : query, "start": start, "end": end, "embedCount": embedCount, "export": "csv"};
		url = "/query/tweets?" + Utils.qs(data); 
			
		window.open(url);
		
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
