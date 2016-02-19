import datetime
import random
import csv
import json

# TODO: Fix * imports
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout

from social.apps.django_app.default.models import UserSocialAuth

from gnip_search.gnip_search_api import QueryError as GNIPQueryError

from chart import Chart
from timeframe import Timeframe
from frequency import Frequency
from tweets import Tweets
from home.utils import *

# import twitter
KEYWORD_RELEVANCE_THRESHOLD = .1    # Only show related terms if > 10%
TWEET_QUERY_COUNT = 10              # For real identification, > 100. Max of 500 via Search API.
DEFAULT_TIMEFRAME = 1              # When not specified or needed to constrain, this # of days lookback
TIMEDELTA_DEFAULT_TIMEFRAME = datetime.timedelta(days=DEFAULT_TIMEFRAME)
TIMEDELTA_DEFAULT_30 = datetime.timedelta(days=30)
DATE_FORMAT = "%Y-%m-%d %H:%M"
DATE_FORMAT_JSON = "%Y-%m-%dT%H:%M:%S"

def login(request):
    """
    Returns login page for given request
    """
    context = {"request": request}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
# @user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/')
def home(request):
    """
    Returns home page for given request
    """
    query = request.GET.get("query", "")
    context = {"request": request, "query0": query}
    tweets = []
    return render_to_response('home.html', context, context_instance=RequestContext(request))

@login_required
def query_chart(request):
    """
    Returns query chart for given request
    """
    # TODO: Move this to one line e.g. queries to query
    query = request.GET.get("query", None)
    queries = request.GET.getlist("queries[]")
    if query:
        queries = [query]

    request_timeframe = Timeframe(start = request.GET.get("start", None),
                                  end = request.GET.get("end", None),
                                  interval = request.GET.get("interval", "hour"))

    response_chart = None
    try:
        response_chart = Chart(queries = queries,
                               start = request_timeframe.start,
                               end = request_timeframe.end,
                               interval = request_timeframe.interval)
    except GNIPQueryError as e:
        return handleQueryError(e)

    response_data = {}
    response_data['days'] = request_timeframe.days
    response_data['start'] = request_timeframe.start.strftime(DATE_FORMAT_JSON)
    response_data['end'] = request_timeframe.end.strftime(DATE_FORMAT_JSON)
    response_data['columns'] = response_chart.columns
    response_data['total'] = response_chart.total

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def query_frequency(request):
    query = request.GET.get("query", None)
    response_data = {}
    sample = 500
    if query is not None:
        
        # Get Timeframe e.g. process time from request
        request_timeframe = Timeframe(start = request.GET.get("start", None),
                                      end = request.GET.get("end", None),
                                      interval = request.GET.get("interval", "hour"))
        
        data = None
        try:
            # Query GNIP and get frequency
            data = Frequency(query = query,
                                  sample = sample,
                                  start = request_timeframe.start,
                                  end = request_timeframe.end)
        except GNIPQueryError as e:
            return handleQueryError(e)
        
        response_data["frequency"] = data.freq
        response_data["sample"] = sample
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def query_tweets(request):
    """
    Returns tweet query
    """
    request_timeframe = Timeframe(start = request.GET.get("start", None),
                                  end = request.GET.get("end", None),
                                  interval = request.GET.get("interval", "hour"))

    query_count = int(request.GET.get("embedCount", TWEET_QUERY_COUNT))
    export = request.GET.get("export", None)
    query = request.GET.get("query", "")
    
    try:
        tweets = Tweets(query=query, query_count=query_count, start=request_timeframe.start, end=request_timeframe.end, export=export)
    except GNIPQueryError as e:
        return handleQueryError(e)
    
    response_data = {}
    if export == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL)
        writer.writerow(['count','time','id','user_screen_name','user_id','status','retweet_count','favorite_count','is_retweet','in_reply_to_tweet_id','in_reply_to_screen_name'])
        count = 0;
        for t in tweets.get_data():
            count = count + 1
            body = t['body'].encode('ascii', 'replace')
            status_id = t['id']
            status_id = status_id[status_id.rfind(':')+1:]
            user_id = t['actor']['id']
            user_id = user_id[user_id.rfind(':')+1:]
            writer.writerow([count, t['postedTime'], status_id, t['actor']['preferredUsername'], user_id, body, t['retweetCount'], t['favoritesCount'], 'X', 'X', 'X'])
        return response
    else:
        response_data['tweets'] = tweets.get_data()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def logout(request):
    """
    Returns a redirect response and logs out user
    """
    auth_logout(request)
    return HttpResponseRedirect('/')

