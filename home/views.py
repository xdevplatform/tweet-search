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
SENTIMENT_THRESHOLD = .6            # .7 is ideal

def login(request):
    
    context = {"request": request}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
def home(request):
    
#     global Classifier.CLASSIFIER_TYPE
#     if not Classifier.CLASSIFIER_TYPE:
#         return redirect("/settings")
    
    context = {"request": request}
    tweets = []

    query = request.REQUEST.get("query", "")
    if query:

        context["query"] = query
        
        g = get_gnip(request.user)

        g.get_repr(query)
        result = g.get_frequency_list(25)
        frequency = []
        for f in result:
            if float(f[3]) >= KEYWORD_RELEVANCE_THRESHOLD:
                frequency.append(f)
        frequency = sorted(frequency, key=lambda f: -f[3]) 
        context["frequency"] = frequency
        
#         print g.get_repr(query, 100, "rate")
#         print g.get_rate()
#         print g.get_repr(query, 50)
#         print g.query_api(query, 10, "json")
#         print g.get_frequency_list(10)
#         print g.query_api(query, use_case = "timeline")
#         print g.get_repr(query, 10, "users")
#         print g.get_rate()
#         print g.get_repr(query, 10, "links")
#         print g.query_api(query, query=True)

        # counts over time
        query_nrt = query
        timeline = g.query_api(query_nrt, 0, "timeline")
        count = 0
        for t in timeline:
            count = count + t["count"]
            t["timePeriod"] = t["timePeriod"][0:8]
        timeline = {
            "count": count,
            "series": json.dumps(timeline)
        }
        context["timeline"] = timeline
        
    tweets = request.REQUEST.get("tweets", "")
    if query and tweets: 

        queryCount = int(request.REQUEST.get("queryCount", TWEET_QUERY_COUNT))
        followersCount = int(request.REQUEST.get("followersCount", 0))
        friendsCount = int(request.REQUEST.get("friendsCount", 0))
        statusesCount = int(request.REQUEST.get("statusesCount", 0))
        favoritesCount = int(request.REQUEST.get("favoritesCount", 0))
        retweets = int(request.REQUEST.get("retweets", 0))
        english = request.REQUEST.get("english", 0)
        klout_score = request.REQUEST.get("klout_score", 0)

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
        positive = 0
        neutral = 0
        negative = 0
        count = 0

        for i in range(len(tweets)):
            
            tweet = json.loads(tweets[i])
            tweets[i] = tweet
            
            if followersCount and tweet["actor"]["followersCount"] < followersCount:
                print "pass followersCount %s" % tweet["actor"]["followersCount"]
                continue

            if friendsCount and tweet["actor"]["friendsCount"] < friendsCount:
                print "pass friendsCount %s" % tweet["actor"]["friendsCount"]
                continue

            if statusesCount and tweet["actor"]["statusesCount"] < statusesCount:
                print "pass statusesCount %s" % tweet["actor"]["statusesCount"]
                continue

            if favoritesCount and tweet["actor"]["favoritesCount"] < favoritesCount:
                print "pass favoritesCount %s" % tweet["actor"]["favoritesCount"]
                continue
            
            body = tweet["body"]
            response = get_sentiment(query, body)
            if response:
                
                count = count + 1

                # top-level sentiment                
                label = response["label"]
                if label == "pos":
                    positive = positive + 1
                elif label == "neg":
                    negative = negative + 1
                else:
                    neutral = neutral + 1

                # pre-curate best/worst tweets
                sentiment = response["probability"][label]
                if sentiment >= SENTIMENT_THRESHOLD:
                    tweet["sentiment"] = sentiment
                    if label == "pos":
                        top.append(tweet)
                    elif label == "neg":
                        bottom.append(tweet)
                        
#                 print label, sentiment, body, json.dumps(tweet)
            
        top = sorted(top, key=lambda t: -t["sentiment"])
        if len(top) > 10:
            top = top[0:10]
            
        bottom = sorted(bottom, key=lambda t: -t["sentiment"])
        if len(bottom) > 10:
            bottom = bottom[0:10]
        
        context["tweets"] = {
             "count": count,
             "positive": int(positive*100/count) if count > 0 else 0,
             "neutral": int(neutral*100/count) if count > 0 else 0,
             "negative": int(negative*100/count) if count > 0 else 0,
             "top" : top,
             "bottom": bottom
         }
        
    integration = {
        "endpoint": "http://localhost:9000/aQ13s4/sentiment",
        "json": "{sentiment: 55%}",
        "web" : "<iframe></iframe>",
        "ios" : "<SOME IOS CODE>",
        "android" : "<SOME ANDROID CODE>",
    }
    context["integration"] = integration

    results = {
       "count" : len(tweets)
    }
    context["results"] = results
    context["queryCount"] = TWEET_QUERY_COUNT
    
    return render_to_response('home.html', context, context_instance=RequestContext(request))

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
def settingsp(request):

    type = request.REQUEST.get("corpus", None)
    if type:
        Classifier.set_classifier(type)
    
    context = {"request": request, "classifier": Classifier.CLASSIFIER_TYPE}
    return render_to_response('settings.html', context, context_instance=RequestContext(request))

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
