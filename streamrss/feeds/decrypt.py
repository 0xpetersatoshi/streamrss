import requests
from bs4 import BeautifulSoup
from streamrss.feeds.base import BaseFeed


class Decrypt(BaseFeed):
    """
    Parses RSS feeds from decrypt.co.
    """

    feed_url: str = "https://decrypt.co/feed"
    feed_name: str = "decrypt"
    entries = None

    def get_entries(self) -> list:
        self.parse()
        self.entries = self.feed.entries
        print(f"number of entries: {len(self.entries)}")
        return self.get_content()

    def get_content(self) -> list:
        new_entries = []
        for entry in self.entries:
            new_entries.append(self._get_entry_content(entry))

        return new_entries

    @staticmethod
    def _get_entry_content(entry: dict) -> dict:
        """
        Returns content for an entry.

        :param entries: A feedparser dict representing an entry
        """
        with requests.Session() as session:
            print(f"making GET request for URL: {entry.link}")
            response = session.get(entry.link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html5lib")
            content = soup.find_all("div", {"class": "z-2"})
            entry["content"] = str(content)

        return entry

