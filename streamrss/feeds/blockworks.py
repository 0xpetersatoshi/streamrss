from streamrss.feeds.base import BaseFeed


class Blockworks(BaseFeed):
    """
    Parses RSS feeds from blockworks.co.
    """

    feed_url: str = "https://blockworks.co/feed"
    feed_name: str = "blockworks"

    def get_entries(self) -> list:
        self.parse()
        return self.feed.entries