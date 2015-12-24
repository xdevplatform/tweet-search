import datetime
import csv
import requests
from django.conf import settings

class Tweets:
    """
    Class container for tweets served to views.py
    """
    def __init__(self, query, query_count, request):
        self.query = query
        self.query_count = query_count
        self.request = request
        self.data = self.get_data()

    def get_data(self):
        """
        Returns tweets
        """
        request = requests.GNIP(request=self.request, query=self.query, query_count=self.query_count)
        return request.get_tweets()
