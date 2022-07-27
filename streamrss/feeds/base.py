from abc import ABC, abstractmethod

import feedparser
from streamrss.feeds import utils


class BaseFeed(ABC):
    """
    A base class representing an RSS feed object.

    :param bookmark: A datetime string for filtering RSS feed entries
    """

    feed: feedparser.FeedParserDict = None
    feed_url: str = None
    feed_name: str = None

    def __init__(self, bookmark: str):
        self.bookmark = bookmark
        self.feedparser = feedparser
        print(f"{self.feed_name} feed initialized with bookmark: {bookmark}")

    def parse(self) -> None:
        """
        Parses the feed URL.
        """
        self.feed = self.feedparser.parse(self.feed_url)

    def get_bookmark(self) -> str:
        """Get the bookmark datestring"""
        return self.bookmark

    def set_bookmark(self, bookmark: str):
        """Set a new bookmark datestring"""
        self.bookmark = bookmark

    def get_filtered_entries(self) -> list:
        """
        Yields feedparser entries that are newer than the bookmark.
        """
        bookmark_dt = utils.strptime_to_utc(self.get_bookmark())
        max_bookmark_dt = bookmark_dt

        print(f"getting feed entries for {self.feed_name}")
        for n, record in enumerate(self.get_entries()):
            # Keep track of the highest/latest published time
            record_bookmark_dt = utils.struct_time_to_datetime(record["published_parsed"])
            max_bookmark_dt = max(record_bookmark_dt, max_bookmark_dt)

            # Only return records that are older than the prior bookmark
            if record_bookmark_dt > bookmark_dt:
                yield record

        # Update the bookmark to the max bookmark datetime found
        self.set_bookmark(max_bookmark_dt.isoformat())

    @abstractmethod
    def get_entries(self) -> list:
        """
        Returns a list of entries.
        """
        raise NotImplementedError
