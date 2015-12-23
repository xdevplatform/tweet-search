from timeseries import Timeseries
from gnip_search.gnip_search_api import GnipSearchAPI
from gnip_search.gnip_search_api import QueryError as GNIPQueryError
from django.conf import settings

class Chart:
    """
    Class for creating line graph chart
    """
    DATE_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self, queries, start, end, interval):
        self.queries = queries
        self.start = start
        self.end = end
        self.interval = interval
        self.total = 0
        self.query_count = 0
        self.x_axis = None
        self.columns = self.create()

    def create(self):
        """
        Returns data in format {"columns": } used in UI
        """
        # New gnip client with fresh endpoint
        g = GnipSearchAPI(settings.GNIP_USERNAME,
                          settings.GNIP_PASSWORD,
                          settings.GNIP_SEARCH_ENDPOINT,
                          paged=True)
        columns = []
        for q in self.queries:
            timeline = None
            try:
                timeline = g.query_api(pt_filter = str(q),
                            max_results = 0,
                            use_case = "timeline",
                            start = self.start.strftime(self.DATE_FORMAT),
                            end = self.end.strftime(self.DATE_FORMAT),
                            count_bucket = self.interval,
                            csv_flag = False)
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

        return columns
