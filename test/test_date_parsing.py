import unittest

from app.strategies.whatsapp_strategy import WhatsAppStrategy


class TestDateParsing(unittest.TestCase):
    testStringDate = "9/24/16, 01:02"

    def test_parse_datetime_hour(self):
        test_datetime = WhatsAppStrategy.parse_datetime(self.testStringDate)
        self.assertEqual(test_datetime.hour, 1)

    def test_parse_datetime_minute(self):
        test_datetime = WhatsAppStrategy.parse_datetime(self.testStringDate)
        self.assertEqual(test_datetime.minute, 2)

    def test_parse_datetime_year(self):
        test_datetime = WhatsAppStrategy.parse_datetime(self.testStringDate)
        self.assertEqual(test_datetime.year, 2016)

    def test_parse_datetime_month(self):
        test_datetime = WhatsAppStrategy.parse_datetime(self.testStringDate)
        self.assertEqual(test_datetime.month, 9)

    def test_parse_datetime_day(self):
        test_datetime = WhatsAppStrategy.parse_datetime(self.testStringDate)
        self.assertEqual(test_datetime.day, 24)


if __name__ == '__main__':
    unittest.main()