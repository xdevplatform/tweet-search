import datetime

class Timeframe:
    """
    The Timeframe class provides a container for timeframe elements required by the GNIP API
    """
    DEFAULT_TIMEFRAME = 90              # When not specified or needed to constrain, this # of days lookback
    TIMEDELTA_DEFAULT_TIMEFRAME = datetime.timedelta(days=DEFAULT_TIMEFRAME)
    TIMEDELTA_DEFAULT_30 = datetime.timedelta(days=30)
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    DATE_FORMAT_JSON = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, start, end, interval):
        self.end = self.get_end(end)
        self.start = self.get_start(start)
        self.interval = interval
        self.days = (self.end-self.start).days

        # if dates wrong, use default
        if self.start > self.end:
            self.start = self.end - self.TIMEDELTA_DEFAULT_TIMEFRAME

    def get_end(self, end):
        """
        Returns processed end date.
        """
        # ensure end always exists
        if not end:
            end = datetime.datetime.now() - datetime.timedelta(minutes=1)
        else:
            end = datetime.datetime.strptime(end, self.DATE_FORMAT)
        return end

    def get_start(self, start):
        """
        Returns processed start date.
        """
        # ensure start always exists
        if not start:
            start = self.end - self.TIMEDELTA_DEFAULT_TIMEFRAME
        else:
            start = datetime.datetime.strptime(start, self.DATE_FORMAT)
        return start

if __name__ == "__main__":
    # Test that Timeframe supplies the output
    time_frame = Timeframe("", "", "")
    print time_frame.start
    print time_frame.end
