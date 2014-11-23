$(function() {

	var evt = isAndroid() || isIOS() ? 'click' : 'tweet';

	twttr.events.bind(evt, function (event) {
	  showResults();
	});

	function showResults () {
	  $('#options-list').addClass('hide');
	  $('#results-list').removeClass('hide');
	}

  function isAndroid () {
     return /Android/i.test(navigator.userAgent);
  }

  function isIOS () {
     return /iPhone|iPad|iPod/i.test(navigator.userAgent);
  }

});