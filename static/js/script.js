$(document).ready(function(){
	
	Page.init();
	if (query0){
		$("#query0").val(query0);
		Page.search();
	}
		
});


var Page = {
		
	maxQueries : 4,

	init : function(query) {

		$("#msg_error").hide();
		$("#msg_success").hide();
		
		$(".loading").hide();
		
		$('.datetimepicker').datetimepicker({
	    	format: 'YYYY-MM-DD HH:mm',
	    	pickTime: true
		});
		
		Page.clear();

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
			Page.toggleTerm("(has:media)", $(this).is(':checked'), false);
		});

		$('#video').on("click", function(){
			Page.toggleTerm("(has:videos)", $(this).is(':checked'), false);
		});

		$("#retweet_help").hide();
		$('#retweet').on("click", function(){
			Page.toggleTerm("-(is:retweet)", $(this).is(':checked'), false);
			if ($(this).is(':checked')){
				$("#retweet_help").fadeIn();
			} else {
				$("#retweet_help").fadeOut();
			}
		});
		
		$(document).on("click", ".term", function(){
			var val = $(this).val();
			var newTerm = "(" + val + ")";
			Page.toggleTerm(newTerm, $(this).is(':checked'), true);
		});
		
	},
	
	toggleTerm : function(term, checked, addIfEmpty){
		$(".query-input").each(function(){
			var query = $(this).val();
			var newTerm = " " + term;
			var finalTerm = ""
			if (checked){
				if (!query && !addIfEmpty){
					return;
				}
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
		$("#terms_frequency").hide();
		$("#chart").html("");
		$("#tweets").html("");
		
		var collapseOptions = $("#collapseOptions.in");
		console.log('collapseOptions: ' + collapseOptions.length);
		
		if (collapseOptions.length > 0){
			console.log(collapseOptions);
			$("#collapseOptions").collapse('hide');
		}

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
		
		Page.hideError();
		
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
				var interval = $("#chart_interval").val();
				Page.loadChart(queries, start, end, interval);
			}

			var queryMashup = "(" + query0 + ")";
			for (var i = 1; i < queries.length; i++){
				if (queries[i]){
					queryMashup = queryMashup + " OR (" + queries[i] + ")" 
				}
			}
			
			if ($("#results_frequency").is(':checked')){
				Page.loadFrequency(queryMashup, start, end);
			}
			
			if ($("#results_tweets").is(':checked')){
				Page.loadTweets(queryMashup, start, end, embedCount);
			}

			if ($("#results_export").is(':checked')){
				Page.loadExport(queryMashup, start, end, embedCount);
			}
}
	},

	loadChart : function(queries, start, end, interval) {

		 $("#chart_loading").show();

	 	 var data = {"start": start, "end": end, "interval": interval};
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
						            		
						            		var iv = x;
						            		if (interval == "hour"){
						            			iv = x / 24;
						            		} 

						            		var date = new Date(start.valueOf());
						            	    date.setDate(date.getDate() + iv);

						            	    var dateStr = (date.getMonth() + 1) + '/' + date.getDate() + '/' +  date.getFullYear()
//					            			console.log(dateStr);
					            			return dateStr;
				            			}
//						                format: '%Y-%m-%d'
						            }
						        }
						    }
						};
					
					// console.log(args);
					var chart = c3.generate(args);
					
					$("#total").html(Utils.integerFormat(response.total));
					$("#activity_volume").fadeIn();
					$("#chart_loading").hide();
					
				},
				error : function(xhr, errorType, exception) {
					Page.handleError(xhr, errorType, exception);
				}
			});
	
	},
	
	loadFrequency : function(query, start, end) {

		$("#terms_frequency").hide();
		$("#frequency_loading").show();
		
	 	var data = {"start": start, "end": end, "query": query};
	 	 
	 	// console.log(data);
		 
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
					// console.log(frequency)
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

						$(".frequency_sample").html(response.sample);
						
						$("#terms_frequency").show();
						$("#frequency_loading").hide();

					}
					
				},
				error : function(xhr, errorType, exception) {
					Page.handleError(xhr, errorType, exception);
				}
			});
	
	},
	
	loadTweets : function(query, start, end, embedCount) {
		
		 $("#tweets_loading").show();
		 var video = $("#video").is(':checked');
		
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
						tweet["class"] = "twitter-tweet";
						
						// uncomment for video tweets
//						if (video){
//							tweet["class"] = "twitter-video";
//						} else {
//							tweet["class"] = "twitter-tweet";
//						}
						
						var output = Mustache.render(template, tweet);
						$("#tweets").append(output);

					}
					
					window.twttr.widgets.load()
					
					$("#activity_tweets").fadeIn();
					
					$("#tweets_loading").hide();
														
				},
				error : function(xhr, errorType, exception) {
					Page.handleError(xhr, errorType, exception);
				}
			});
		 
	},
	
	loadExport : function(query, start, end, embedCount) {
		
		data = {"query" : query, "start": start, "end": end, "embedCount": embedCount, "export": "csv"};
		url = "/query/tweets?" + Utils.qs(data); 
			
		window.open(url);
		
	},
	
	showError : function (msg, small){
		
		template = $("#temlateMessageError").html();
		Mustache.parse(template);
		
		var body = {"message": msg}
		if (small){
			body['helper'] = "Original query: '"+small+"'"  
		}
		var output = Mustache.render(template, body);
	
		$("div.container div.main").prepend(output);
		$(".loading").hide();

//		$("#msg_error div.msg").html(msg);
//		$("#msg_error").fadeIn();
	},

	hideError : function (msg){
		$(".msg_error").hide();
	},

	handleError : function(xhr, errorType, exception){
		
		console.log('Error occured');
		console.log(xhr.responseJSON.error);
		console.log(xhr.responseJSON.payload);
		
		var helper = "";
		if (xhr.responseJSON.payload && xhr.responseJSON.payload.query){
			helper = xhr.responseJSON.payload.query;
		}
		
		Page.showError(xhr.responseJSON.error, helper);
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
