import json

from django.http import HttpResponse
from django.conf import settings

from gnip_search.gnip_search_api import GnipSearchAPI

def get_gnip(paged=False):
    """
    Returns Gnip Search API
    """
    g = GnipSearchAPI(settings.GNIP_USERNAME,
        settings.GNIP_PASSWORD,
        settings.GNIP_SEARCH_ENDPOINT,
        paged=paged)
    return g

def handleQueryError(e):
    
    response_data = {}
    response_data['error'] = e.message
    response_data['response'] = e.response
    response_data['payload'] = e.payload
    
    print response_data
    
    return HttpResponse(json.dumps(response_data), status=400, content_type="application/json")
