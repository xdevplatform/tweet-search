import datetime
import random
import csv
import json

from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from social.apps.django_app.default.models import UserSocialAuth

from gnip_search.gnip_search_api import *

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
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/')
def home(request):
    
    query = request.REQUEST.get("query", "")
    context = {"request": request, "query0": query}
    tweets = []

    return render_to_response('home.html', context, context_instance=RequestContext(request))

@login_required
def query_chart(request):

    response_data = {}

    (start, end, interval, days) = get_timeframe(request)
        
    response_data['days'] = days
    response_data['start'] = start.strftime(DATE_FORMAT_JSON)
    response_data['end'] = end.strftime(DATE_FORMAT_JSON)

    query = request.REQUEST.get("query", "")
    queries = request.REQUEST.getlist("queries[]")
    
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

    # New gnip client with fresh endpoint
    g = get_gnip(request.user)
        
    if query:
        queries = [query]
        
    total = 0
    queryCount = 0
    xAxis = None
    columns = []
    
    for q in queries:

        queryTotal = 0
        queryCount = queryCount + 1

        timeline = None
        try:
            timeline = g.query_api(q, 0, use_case="timeline", start=start.strftime(DATE_FORMAT), end=end.strftime(DATE_FORMAT), count_bucket=interval, csv_flag=False)
        except QueryError as e:
            return handleQueryError(e);

        timeline = json.loads(timeline)
    
        series = [] 
        for t in timeline['results']:
            
            t_count = t["count"]
            series.append(t_count)
            queryTotal = queryTotal + t_count
            
        label = q[0:30]
        if len(q) > 30:
            label = label + "..."
        label = label + " (" + str(queryTotal) + ")"
        series.insert(0, label)
        columns.append(series)
        
        total = total + queryTotal

        # only build timetable xAxis once
        if not xAxis:      
            xAxis = ['']
            for t in timeline['results']:
                tp = t["timePeriod"]
                
                day = str(tp[0:4] + "-" + tp[4:6] + "-" + tp[6:8] + " " + tp[8:10] + ":" + "00:00")
                
                xAxis.append(day)
                columns.insert(0, xAxis)
                
    response_data['columns'] = columns
    response_data['total'] = total
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
        
@login_required
def query_frequency(request):

    sample = 500
    response_data = {}
    
    (start, end, interval, days) = get_timeframe(request)
    
    query = request.REQUEST.get("query", "")
    if query:

        # New gnip client with fresh endpoint (this one sets to counts.json)
        g = get_gnip(request.user)
        
        timeline = None
        try:
            timeline = g.query_api(query, sample, use_case="wordcount", start=start.strftime(DATE_FORMAT), end=end.strftime(DATE_FORMAT), csv_flag=False)
        except QueryError as e:
            return handleQueryError(e);

        frequency = []
        result = g.freq.get_tokens(20)
        for f in result:
            frequency.append(f)
#             if float(f[3]) >= KEYWORD_RELEVANCE_THRESHOLD:
#                 frequency.append(f)
        frequency = sorted(frequency, key=lambda f: -f[3]) 
        response_data["frequency"] = frequency
        response_data["sample"] = sample
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")
        
@login_required
def query_tweets(request):

    response_data = {}
    
    (start, end, interval, days) = get_timeframe(request)

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
        
        # scrub tweet display query for no retweets 
        not_rt = "-(is:retweet)"
        if (not_rt not in query_nrt):
            query_nrt = query_nrt.replace("is:retweet", "")
            query_nrt = "%s %s" % (query_nrt, not_rt)  

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
        
        tweets = None

        try:
            tweets = g.query_api(query_nrt, queryCount, use_case="tweets", start=start.strftime(DATE_FORMAT), end=end.strftime(DATE_FORMAT))
        except QueryError as e:
            return handleQueryError(e);

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

def get_timeframe(request):

    start = request.REQUEST.get("start", "")
    end = request.REQUEST.get("end", "")
    interval = request.REQUEST.get("interval", "hour")
    days = DEFAULT_TIMEFRAME
    
    # ensure end always exists
    if not end:
        end = datetime.datetime.now() - datetime.timedelta(minutes=1)
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

    days = (end-start).days 
        
    return (start, end, interval, days)

def handleQueryError(e):
    
    response_data = {}
    response_data['error'] = e.message
    response_data['response'] = e.response
    response_data['payload'] = e.payload
    
    print response_data
    
    return HttpResponse(json.dumps(response_data), status=400, content_type="application/json")


from django.contrib.auth import logout as auth_logout
def logout(request):
    
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def get_gnip(user):
    
    g = GnipSearchAPI(settings.GNIP_USERNAME,
        settings.GNIP_PASSWORD,
        settings.GNIP_SEARCH_ENDPOINT)

    return g
