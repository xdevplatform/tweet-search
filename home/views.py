import datetime
import random
import json

from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from social.apps.django_app.default.models import UserSocialAuth

from gnip_search import gnip_search_api
from engine.models import Classifier

# import twitter

KEYWORD_RELEVANCE_THRESHOLD = .1    # Only show related terms if > 10%
TWEET_QUERY_COUNT = 10              # For real identification, > 100. Max of 500 via Search API.
DEFAULT_TIMEFRAME = 14              # 2 weeks lookback default
DATE_FORMAT = "%Y-%m-%d %H:%M"
DATE_FORMAT_JSON = '%Y-%m-%dT%H:%M:%S'

def login(request):
    
    context = {"request": request}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
def home(request):
    
    context = {"request": request}
    tweets = []

    return render_to_response('home.html', context, context_instance=RequestContext(request))

@login_required
def query_chart(request):

    response_data = {}

    query = request.REQUEST.get("query", "")
    
    if query:

        start = request.REQUEST.get("start", "")
        end = request.REQUEST.get("end", "")
        days = DEFAULT_TIMEFRAME
        
        # ensure end always exists
        if not end:
            end = datetime.datetime.now()
        else:
            end = datetime.datetime.strptime(end, DATE_FORMAT)

        # ensure start always exists        
        if not start:
            start = end - datetime.timedelta(days=DEFAULT_TIMEFRAME)
        else:
            start = datetime.datetime.strptime(start, DATE_FORMAT)

        # if dates wrong, use default            
        if start > end:
            start = end - datetime.timedelta(days=DEFAULT_TIMEFRAME)
            
        g = get_gnip(request.user)

        g.get_repr(query)
        result = g.get_frequency_list(25)
        frequency = []
        for f in result:
            if float(f[3]) >= KEYWORD_RELEVANCE_THRESHOLD:
                frequency.append(f)
        frequency = sorted(frequency, key=lambda f: -f[3]) 
        response_data["frequency"] = frequency
        
        # c3 data format for timeseries (http://c3js.org/samples/timeseries.html)
        #     data: {
        #         x: 'x',
        # //        xFormat: '%Y%m%d', // 'xFormat' can be used as custom format of 'x'
        #         columns: [
        #             ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
        # //            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
        #             ['data2', 130, 340, 200, 500, 250, 350]
        #         ]
        #     },

        # counts over time
        query_nrt = query
        
        days = (end-start).days 
        start_str = start.strftime(DATE_FORMAT)
        end_str = end.strftime(DATE_FORMAT)
        
        timeline = g.query_api(query_nrt, 0, "timeline", start=start_str, end=end_str, count_bucket="hour")
        x = ['x']
        series = ['count']

        total = 0
        for t in timeline:
            
            t_count = t["count"]
            series.append(t_count)
            total = total + t_count

            tp = t["timePeriod"]
            day = str(tp[0:4] + "-" + tp[4:6] + "-" + tp[6:8] + " " + tp[8:10] + ":" + "00:00")
            x.append(day)
            
        response_data['columns'] = [x, series]
        response_data['total'] = total
        response_data['days'] = days
        response_data['start'] = start.strftime(DATE_FORMAT_JSON)
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")
        
@login_required
def query_tweets(request):

    response_data = {}

    queryCount = int(request.REQUEST.get("queryCount", TWEET_QUERY_COUNT))
    followersCount = int(request.REQUEST.get("followersCount", 0))
    friendsCount = int(request.REQUEST.get("friendsCount", 0))
    statusesCount = int(request.REQUEST.get("statusesCount", 0))
    favoritesCount = int(request.REQUEST.get("favoritesCount", 0))
    retweets = int(request.REQUEST.get("retweets", 0))
    english = request.REQUEST.get("english", 0)
    klout_score = request.REQUEST.get("klout_score", 0)

    query = request.REQUEST.get("query", "")
    if query:

        g = get_gnip(request.user)

        query_nrt = query

#         if followersCount:
#             query_nrt = query_nrt + " (followers_count:%s)" % followersCount
#         if friendsCount:
#             query_nrt = query_nrt + " (friends_count:%s)" % friendsCount
#         if statusesCount:
#             query_nrt = query_nrt + " (statuses_count:%s)" % statusesCount
#         if favoritesCount:
#             query_nrt = query_nrt + " (favorites_count:%s)" % favoritesCount
        if not retweets:
            query_nrt = query_nrt + " -(is:retweet)"
        if english:
            query_nrt = query_nrt + " (lang:en)" 
        if klout_score:
            query_nrt = query_nrt + " klout_score:%s" % klout_score
    
        print "%s (%s)" % (query_nrt, queryCount)
    
        # last N tweets, categorized by sentiment
        top = []
        bottom = []
        tweets = []
        tc = 0
        
        if queryCount > 500:
            g.paged = True
            
        while tc < queryCount:
            tweets_cursor = g.query_api(query_nrt, queryCount)
            tweets = tweets + tweets_cursor
            tc = len(tweets)
            print "query paging: %s " % tc  
            
        for i in range(len(tweets)):
            tweets[i] = json.loads(tweets[i])

        response_data['tweets'] = tweets
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_sentiment(query, body):

    query = query.lower()
    body = body.lower()
    
    # scrub query from body
    query = query.replace("(", "")
    query = query.replace(")", "")
    query = query.replace(" or ", " ")
    query = query.split(" ")
    
    for q in query:
        body = body.replace(q, "")

    return Classifier.get_sentiment(body)

from django.contrib.auth import logout as auth_logout
def logout(request):
    
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def get_gnip(user):
    
    g = gnip_search_api.GnipSearchAPI(settings.GNIP_USERNAME,
        settings.GNIP_PASSWORD,
        settings.GNIP_SEARCH_ENDPOINT)

    return g
