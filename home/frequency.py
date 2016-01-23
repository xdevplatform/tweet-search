from django.conf import settings
from gnip_search.gnip_search_api import GnipSearchAPI
from gnip_search.gnip_search_api import QueryError as GNIPQueryError

class Frequency:
    """
    Class collection for Frequency
    """
    DATE_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self, query, sample, start, end):
        self.query = query
        self.sample = sample
        self.start = start
        self.end = end
        self.freq = self.get(self.get_data())

    def get_data(self):
        """
        Returns data for frequency in list view
        """
        # New gnip client with fresh endpoint (this one sets to counts.json)

        g = GnipSearchAPI(settings.GNIP_USERNAME,
                          settings.GNIP_PASSWORD,
                          settings.GNIP_SEARCH_ENDPOINT,
                          paged=False)
        timeline = None
        try:
            timeline = g.query_api(self.query, self.sample, use_case="wordcount", start=self.start.strftime(self.DATE_FORMAT), end=self.end.strftime(self.DATE_FORMAT), csv_flag=False)
        except GNIPQueryError as e:
            print(e);

        result = g.freq.get_tokens(20)
        return result

    def get(self, data):
        response_data = []
        for f in data:
            response_data.append(f)
        response_data = sorted(response_data, key=lambda f: -f[3])
        return response_data
