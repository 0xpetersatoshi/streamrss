from abc import ABC, abstractmethod
from datetime import datetime
from time import mktime, struct_time

import feedparser


class BaseFeed(ABC):
    """
    A base class representing an RSS feed object.

    :param config: A dictionary containing configuration parameters
    """

    feed: feedparser.FeedParserDict = None
    feed_url: str = None

    def __init__(self, config: dict = None):
        self.config = config
        self.feedparser = feedparser

    def parse(self) -> None:
        """
        Parses the feed URL.
        """
        self.feed = self.feedparser.parse(self.feed_url)

    def get_filtered_entries(self, entries: list) -> list:
        """
        Returns a filtered list of entries that match a specific regex pattern
        in the config.

        :param entries: A list of feedparser entries
        """
        pass

    @abstractmethod
    def get_entries(self) -> list:
        """
        Returns a list of entries.
        """
        raise NotImplementedError

    @staticmethod
    def struct_time_to_datetime(t: struct_time) -> datetime:
        """
        Converts time.struct_time objects to datetime objects.

        :param t: A time.struct_time object
        """
        return datetime.fromtimestamp(mktime(t))
