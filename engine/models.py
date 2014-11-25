import requests
import json

from django.conf import settings

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

class Classifier:

    # default to text-processing
    CLASSIFIER_TYPE = "tp"
    CLASSIFIER = None

    @staticmethod
    def set_classifier(type):
        Classifier.CLASSIFIER_TYPE = type
        
    @staticmethod
    def get_sentiment(text):        
        
        if Classifier.CLASSIFIER_TYPE == "tp":
            return Classifier.get_sentiment_tp(text)
        
        if Classifier.CLASSIFIER_TYPE == "movies":
            return Classifier.get_sentiment_movies(text)
            
        return None

    @staticmethod
    def get_sentiment_tp(body):
        
        url = "https://japerk-text-processing.p.mashape.com/sentiment/"
        headers = {
          "X-Mashape-Key": settings.MASHAPE_KEY,
          "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
          "language": "english",
          "text": body
        }
    
        r = requests.post(url, data=params, headers=headers)
        
        result = None
        if r and r.text:
            result = json.loads(r.text)
            
        return result
    
    @staticmethod
    def get_sentiment_movies(text):
    
        def word_feats(words):
            return dict([(word, True) for word in words])
         
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')
         
        negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
         
        negcutoff = len(negfeats) * 3 / 4
        poscutoff = len(posfeats) * 3 / 4
         
        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
        print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
        
        Classifier.CLASSIFIER = NaiveBayesClassifier.train(trainfeats)
        
    #         print 'accuracy:', nltk.classify.util.accuracy(CLASSIFIER, testfeats)
    #         CLASSIFIER.show_most_informative_features()
    
        print Classifier.CLASSIFIER.classify(word_feats('This is the best thing ever'))
        print Classifier.CLASSIFIER.classify(word_feats('I hate the world'))
    
    @staticmethod
    def document_features(document, word_features):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features
