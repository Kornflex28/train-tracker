import datetime as dt


class DateTime(dt.datetime):

    def to_tdate(self) -> str:
        """
        Convert datetime object to string T date format
        :param date: Date to convert. dt.datetime object
        :return: date string, format: %Y-%m-%dT%H:%M:%S
        """
        return self.strftime("%Y-%m-%dT%H:%M:%S")

    def to_date(self) -> str:
        """
        Convert datetime object to string date format
        :param date: Date to convert. dt.datetime object
        :return: date string, format: %Y-%m-%d %H:%M:%S
        """
        return self.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def tdate_to_date(tdate: str) -> str:
        """
        Convert T date string object to date string
        :param tdate: date string, format: %Y-%m-%dT%H:%M:%S
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