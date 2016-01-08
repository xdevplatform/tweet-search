import json

#TODO: Clean and place functions on each self instead of one huge statement

class Timeseries:
    """
    Class to produce timeseries data
    """
    def __init__(self, query, timeline, columns, total, xAxis=None):
        self.columns = columns
        self.query = query
        self.timeline = json.loads(timeline)
        self.query_total = 0
        self.series = self.create_series()
        self.columns.append(self.series)
        self.total = total + self.query_total
        self.xAxis = self.create_x_axis(xAxis)

    def create_series(self):
        """
        Returns a series based on `results` from timeline
        """
        series = []
        for timeline_object in self.timeline['results']:
            count = timeline_object["count"]
            series.insert(0, count)
            self.query_total = self.query_total + count
        label = self.query[0:30]
        if len(self.query) > 30:
            label = label + "..."
        label = label + " (" + str(self.query_total) + ")"
        series.insert(0, label)
        return series

    def create_x_axis(self, xAxis):
        """
        Returns xAxis for timeseries
        """
        if not xAxis:
            xAxis = []
            for t in self.timeline['results']:
                time_period = t["timePeriod"]
                day = str(time_period[0:4] + "-" +
                          time_period[4:6] + "-" +
                          time_period[6:8] + " " +
                          time_period[8:10] + ":" +
                          "00:00")
                xAxis.append(day)
        return xAxis

if __name__ == "__main__":
    ts = Timeseries(query="gareth",
               timeline="""{"results": [{"count": 268477, "timePeriod": "201512220000"},  {"count": 316681, "timePeriod": "201512210000"}]}""",
               columns=[],
               total=0)
    print ts.columns
