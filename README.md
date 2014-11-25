Twitter Reviews Everywhere
=================

Sample Django App using GNIP to power Twitter reviews for anything via GNIP.

Large portions of this sample code are based on Laurent Luce's great
Twitter + NLTK blog here: http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/


Requirements
============

To run this sample code, you'll need to install the following libraries:

- `pip install south` (http://south.aeracode.org/)
- `pip install fabric` (http://www.fabfile.org/)
- `pip install gapi` (https://github.com/DrSkippy/Gnip-Python-Search-API-Utilities)
` `pip install nltk` (http://www.nltk.org/)

After installing nltk, run the following in the command line

	import nltk
	nltk.download()
	d movie_reviews

Getting Started
============

- Create a Twitter App (https://apps.twitter.com/)

- Specify your GNIP credentials in app/settings.py under the following section:

    GNIP_USERNAME = 'YOUR_GNIP_USERNAME'
    GNIP_PASSWORD = 'YOUR_GNIP_PASSWORD'
    GNIP_SEARCH_ENDPOINT = 'YOUR_GNIP_SEARCH_ENDPOINT'

- To initialize your database, run the from the `reviews-everywhere` directory:

  python manage.py syncdb

- To start the server, run the following from the `reviews-everywhere` directory:

  fab start
  
- Open a browser and go to http://localhost:9000

Notes
============
If you receive a 401 at login/twitter it is most likely caused by a datetime discrepancy between the server making the requst and the Twitter server.

Use NTP to sync time on your server to compensate for the drift.

If you are getting this error on OSX, toggle the "set time zone" checkbox off and back on in Date & Time system preferences for a manual and temporary fix. It has been reported that OSX 10.9 Mavericks has an issue with time drift.
