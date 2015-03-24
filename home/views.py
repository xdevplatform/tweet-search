import datetime
import random
import csv
import json

from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from social.apps.django_app.default.models import UserSocialAuth

from gnip_search import gnip_search_api

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

    query = request.REQUEST.get("query", "")
    queries = request.REQUEST.get("queries", "")
    
    if query:

        # New gnip client with fresh endpoint (this one sets to counts.json)
        g = get_gnip(request.user)
        
        timeline = g.query_api(query, 100, use_case="wordcount", csv_flag=False)
        
        frequency = []
        result = g.freq.get_tokens(20)
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
        
    if not queries:

        # New gnip client with fresh endpoint
        g = get_gnip(request.user)

        days = (end-start).days 
        start_str = start.strftime(DATE_FORMAT)
        end_str = end.strftime(DATE_FORMAT)
        
        timeline = g.query_api(query, 0, use_case="timeline", start=start_str, end=end_str, count_bucket="hour", csv_flag=False)
        timeline = json.loads(timeline)
        
        x = ['x']
        series = ['count']

        total = 0
        for t in timeline['results']:
            
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
    queryCount = int(request.REQUEST.get("embedCount", TWEET_QUERY_COUNT))
    
#     followersCount = int(request.REQUEST.get("followersCount", 0))
#     friendsCount = int(request.REQUEST.get("friendsCount", 0))
#     statusesCount = int(request.REQUEST.get("statusesCount", 0))
#     favoritesCount = int(request.REQUEST.get("favoritesCount", 0))
#     retweets = int(request.REQUEST.get("retweets", 0))
#     english = request.REQUEST.get("english", 0)
#     klout_score = request.REQUEST.get("klout_score", 0)

    export = request.REQUEST.get("export", None)
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
#         if not retweets:
#             query_nrt = query_nrt + " -(is:retweet)"
#         if english:
#             query_nrt = query_nrt + " (lang:en)" 
#         if klout_score:
#             query_nrt = query_nrt + " klout_score:%s" % klout_score
    
        print "%s (%s)" % (query_nrt, queryCount)
    
        if queryCount > 500:
            g.paged = True
        tweets = g.query_api(query_nrt, queryCount, use_case="tweets")
        tc = len(tweets)

        print "total size: %s " % tc  

#         for i in range(len(tweets)):
#             tweets[i] = json.loads(tweets[i])
        
    if export == "csv":
        
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
    
        writer = csv.writer(response)
        writer.writerow(['count','time','id','user_screen_name','user_id','status','retweet_count','favorite_count','is_retweet','in_reply_to_tweet_id','in_reply_to_screen_name'])
        
        count = 0;
        for t in tweets:
            count = count + 1
            body = t['body'].encode('ascii', 'replace')
            status_id = t['id']
            status_id = status_id[status_id.rfind(':')+1:]
            user_id = t['actor']['id']
            user_id = user_id[user_id.rfind(':')+1:]
            writer.writerow([count, t['postedTime'], status_id, t['actor']['preferredUsername'], user_id, body, t['retweetCount'], t['favoritesCount'], 'X', 'X', 'X'])
            
    
        return response
        
    else:
        
        response_data['tweets'] = tweets
        return HttpResponse(json.dumps(response_data), content_type="application/json")

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
