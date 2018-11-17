import datetime as dt


class Date:

    @staticmethod
    def datetime_to_tdate(date: dt.datetime) -> str:
        """
        Convert datetime object to string T date format
        :param date: Date to convert. dt.datetime object
        :return: date string, format: %Y-%m-%dT%H:%M:%S
        """
        return date.strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def datetime_to_date(date: dt.datetime) -> str:
        """
        Convert datetime object to string date format
        :param date: Date to convert. dt.datetime object
        :return: date string, format: %Y-%m-%d %H:%M:%S
        """
        return date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def date_to_datetime(date: str) -> dt.datetime:
        """
        Convert date string object to datetime
        :param date: date string, format: %Y-%m-%d %H:%M:%S
        :return: Date to convert. dt.datetime object
        """
        return dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def tdate_to_datetime(tdate: str) -> dt.datetime:
        """
        Convert T date string object to datetime
        :param date: date string, format: %Y-%m-%dT%H:%M:%S
        :return: Date to convert. dt.datetime object
        """
        return dt.datetime.strptime(tdate, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def tdate_to_date(tdate: str) -> str:
        """
        Convert T date string object to date string
        :param date: date string, format: %Y-%m-%dT%H:%M:%S
        :return: date string, format: %Y-%m-%d %H:%M:%S
        """
        return dt.datetime.strptime(tdate, "%Y-%m-%dT%H:%M:%S") \
            .strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def date_to_tdate(date: str) -> str:
        """
        Convert date string object to T date string
        :param date: date string, format: %Y-%m-%d %H:%M:%S
        :return: date string, format: %Y-%m-%dT%H:%M:%S
        """
        return dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") \
            .strftime("%Y-%m-%dT%H:%M:%S")