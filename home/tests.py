import unittest
import timeframe
import timeseries
import datetime
import frequency
#from django.test import TestCase

# Create your tests here.
class Tests(unittest.TestCase):
    """
    Class for tests
    """
    def setUp(self):
        pass

    def test_timeframe(self):
        empty_timeframe = timeframe.Timeframe("", "", "")
        self.assertEqual(type(empty_timeframe.start), datetime.datetime)
        self.assertEqual(type(empty_timeframe.end), datetime.datetime)

    def test_timeseries(self):
        ts = timeseries.Timeseries(query="one direction",
                   timeline="""{"results": [{"count": 268477, "timePeriod": "201512220000"},  {"count": 316681, "timePeriod": "201512210000"}]}""",
                   columns=[],
                   total=0)
        self.assertEqual(type(ts.columns), list)

    def test_chart(self):
        # TODO: fix chart
        request_timeframe = timeframe.Timeframe(start = "", end = "", interval = "")
        queries = ["#TwitterDev"]
        self.assertEqual(type(queries), list)

    def test_frequency(self):
        # TODO: fix with GNIP
        request_timeframe = timeframe.Timeframe(start = "", end = "", interval = "")
        frequency = []
        self.assertEqual(type(frequency), list)

if __name__ == '__main__':
    unittest.main()
