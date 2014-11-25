import random
import json

from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from social.apps.django_app.default.models import UserSocialAuth

from gnip_search import gnip_search_api

# import twitter

FREQUENCY_THRESHOLD = .1
CLASSIFIER = None

def login(request):
    
    context = {"request": request}
    return render_to_response('login.html', context, context_instance=RequestContext(request))

@login_required
def home(request):
    
    global CLASSIFIER
    if not CLASSIFIER:
        return redirect("/learning")
    
    context = {"request": request}
    tweets = []

    query = request.REQUEST.get("query", "")
    context["query"] = query
    
    if query:
        
        g = get_gnip(request.user)

        g.get_repr(query)
        result = g.get_frequency_list(25)
        frequency = []
        for f in result:
            if float(f[3]) >= FREQUENCY_THRESHOLD:
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
        timeline = g.query_api(query, 0, "timeline")
        context["timeline"] = timeline
        
        # last N tweets, categorized by sentiment
        top = []
        bottom = []
        tweets = g.query_api(query, 100)

        for i in range(len(tweets)):
            
            tweet = json.loads(tweets[i])
            tweets[i] = tweet
            
            sentiment = random.random()
            tweet["sentiment"] = sentiment
             
            if tweet["sentiment"] > .5:
                top.append(tweet)
            else:
                bottom.append(tweet)
            
        top = sorted(top, key=lambda t: -t["sentiment"])
        if len(top) > 10:
            top = top[0:10]
            
        bottom = sorted(bottom, key=lambda t: t["sentiment"])
        if len(bottom) > 10:
            bottom = bottom[0:10]
        
        context["tweets"] = {
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
    
    return render_to_response('home.html', context, context_instance=RequestContext(request))

from django.contrib.auth import logout as auth_logout
def learning(request):

    if request.REQUEST.get("corpus", None) == 'movies':
        
        import nltk.classify.util
        from nltk.classify import NaiveBayesClassifier
        from nltk.corpus import movie_reviews
         
        def word_feats(words):
            return dict([(word, True) for word in words])
         
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')
         
        negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
         
        negcutoff = len(negfeats)*3/4
        poscutoff = len(posfeats)*3/4
         
        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
        print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
        
        global CLASSIFIER 
        CLASSIFIER = NaiveBayesClassifier.train(trainfeats)
        
#         print 'accuracy:', nltk.classify.util.accuracy(CLASSIFIER, testfeats)
#         CLASSIFIER.show_most_informative_features()

        print CLASSIFIER.classify(word_feats('This is the best thing ever'))
        print CLASSIFIER.classify(word_feats('I hate the world'))

    context = {"request": request}
    return render_to_response('learning.html', context, context_instance=RequestContext(request))

def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

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


    return api