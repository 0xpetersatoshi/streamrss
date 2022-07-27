from streamrss.feeds import FEEDS, utils


class FeedHandler:
    """A wrapper class to handle looping through the RSS feed classes
    and getting/setting state.
    
    :param state: A dictionary containing the feed state (bookmarks)
    """

    def __init__(self, state: dict) -> None:
        self.state = state

    def get_feeds(self):
        """Loops through all the feed objects, instantiates, and runs them."""

        state = self.get_state()

        # Loop through all the feed objects, instantiate them, and run
        # their get_filtered_entries method to start fetching RSS feeds
        for feed in FEEDS:
            # Get the latest bookmark for each feed object and pass it
            # to the object to filter for feeds newer than the bookmark datetime
            bookmark = utils.get_bookmark(state, feed)
            feed_obj = FEEDS[feed](bookmark)
            yield from feed_obj.get_filtered_entries()

            # Get the latest bookmark and update the state object
            bookmark = feed_obj.get_bookmark()
            self.set_state(utils.write_bookmark(state, feed, bookmark))

    def set_state(self, state: dict):
        self.state = state

    def get_state(self) -> dict:
        return self.state
