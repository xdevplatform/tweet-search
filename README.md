Tweet Search
=================

This sample uses GNIP full archive search to show the activity volume and latest tweets on any given topic. It also renders tweets using Twitter's widgets.js.

<img src="screenshot.png" style="width: 70%;"/>

As always, when developing on top of the Twitter platform, you must abide by the [Developer Agreement & Policy](https://dev.twitter.com/overview/terms/agreement-and-policy). 

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/twitterdev/tweet-search)


Requirements
============

To run this sample code, you can install the required libraries with:

	`pip install -r requirements.txt`

Getting Started
============

- Create a Twitter App (https://apps.twitter.com/). Also, ensure that the Callback URL is populated. This can point to http://localhost:9000 to start. If it is not included, you will get Client Authorization errors upon login.

- Specify your API and GNIP credentials in app/settings.py under the following section:

    GNIP_USERNAME = 'YOUR_GNIP_USERNAME'
    GNIP_PASSWORD = 'YOUR_GNIP_PASSWORD'
    GNIP_SEARCH_ENDPOINT = 'YOUR_GNIP_SEARCH_ENDPOINT'
	
- To initialize your database, run the from the `tweet-search` directory:

  `python manage.py syncdb`
  
  Then run:
  
  `python manage.py migrate --settings=app.settings_my`

- To start the server, run the following from the `tweet-search` directory:

  `fab start`
  
- Open a browser and go to http://localhost:9000

Note that the GNIP_SEARCH_ENDPOINT is a URL to the full archive search URL, and is in the format `https://data-api.twitter.com/search/fullarchive/...`.
If you want to use the 30-day search, open the `gnip_search_api.py` file, search for the term "30 DAY" and follow the instructions. (You also need to 
use the 30-day search URL, and not the full arhive search URL.)

Sample Queries
============

Some sample queries to run:

- Hashtag search (default AND): `#MLB #SFGiants`
- Mention search, no retweets: `@TwitterDev -(is:retweet)`
- Search with images/videos: `walking dead (has:media)`

Advanced Options
============

In the UI, there is a link to show advanced options. Specifically:

- Start/end dates. GNIP search allows a variable timeframe to search. For optimal results, 30 days will return a response in a reasonable timeframe.
- Has media. This appends `(has:media)` to your query 

<img src="advanced.png" style="width: 70%;"/>

Related Terms
============

The GNIP search can also suggest additional related terms to add to your query. Click on the 'related terms' 
link and a drop-down will appear to suggest (and add) additional terms to your query:

<img src="terms.png" style="width: 70%;"/>
