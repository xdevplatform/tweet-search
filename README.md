ratings-everywhere

=================

Sample Django App using GNIP to power Twitter ratings for anything via GNIP.

REQUIREMENTS
============

To run this sample code, you'll need to install the following libraries:

- Python Social Auth (https://github.com/omab/python-social-auth)
- Python Twitter (https://github.com/bear/python-twitter)
- south (http://south.aeracode.org/)
- Fabric (http://www.fabfile.org/)

GETTING STARTED
============

- Create a Twitter App (https://apps.twitter.com/)
- Specify your Twitter App tokens in app/settings.py under the following section:

    SOCIAL_AUTH_TWITTER_KEY = 'YOUR_TWITTER_API_KEY'
    SOCIAL_AUTH_TWITTER_SECRET = 'YOUR_TWITTER_API_SECRET'
    
    TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
    TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

- To initialize your database, run the from the `ratings-everywhere` directory:

  python manage.py syncdb

- To start the server, run the following from the `ratings-everywhere` directory:

  fab start
  
- Open a browser and go to http://localhost:9000

NOTES
============
If you receive a 401 at login/twitter it is most likely caused by a datetime discrepancy between the server making the requst and the Twitter server.

Use NTP to sync time on your server to compensate for the drift.

If you are getting this error on OSX, toggle the "set time zone" checkbox off and back on in Date & Time system preferences for a manual and temporary fix. It has been reported that OSX 10.9 Mavericks has an issue with time drift.
