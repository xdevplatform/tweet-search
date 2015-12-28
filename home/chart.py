#TODO: WRITE TESTS
from timeseries import Timeseries
from gnip_search.gnip_search_api import GnipSearchAPI
from gnip_search.gnip_search_api import QueryError as GNIPQueryError
from django.conf import settings
import requests

class Chart:
    """
    Class for creating line graph chart
    """
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    DATE_FORMAT_JSON = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, queries, request):
        self.queries = queries
        self.request = request
        self.total = 0
        self.query_count = 0
        self.x_axis = None
        self.data = self.create()

    def create(self):
        """
        Returns data in format {"columns": } used in UI
        """
        data = {}
        columns = []
        for q in self.queries:

            timeline = None
            try:
                request = requests.GNIP(request=self.request, query=q)
                timeline = request.get_timeline()
                if 'start' not in data:
                    data['start'] = request.start.strftime(self.DATE_FORMAT_JSON)
                if 'end' not in data:
                    data['end'] = request.end.strftime(self.DATE_FORMAT_JSON)
                if 'days' not in data:
                    data['days'] = request.days

            except GNIPQueryError as e:
                print e

            # Process timeseries on the GNIP Data
            time_series_data = Timeseries(q, timeline, columns, self.total, self.x_axis)
            column = time_series_data.columns

            if self.x_axis == None:
                self.x_axis = time_series_data.xAxis
                columns.insert(0, self.x_axis)

            columns.append(time_series_data.series)
            self.total = time_series_data.total

        data['columns'] = columns
        data['total'] = self.total
        return data
