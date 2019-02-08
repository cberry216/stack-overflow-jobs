import feedparser
import ssl


class RSSParser:
    def __init__(self, url):
        """
        Initializer for RSSParser class.

        Arguments:
            url {str} -- URL for RSSParser to parse.
        """

        self.url = url
        self.feed, self.keys, self.entries = self.parse_rss_feed()
        self.count = len(self.entries)

    def parse_rss_feed(self):
        """
        Parses the provided URL.

        Returns:
            feedparser.FeedParserDict -- Dictionary containing the entire parsed RSS feed, headers and all.
            dict_keys -- List of the parsed feeds dictionary keys (used for exception checking).
            list -- List of all entries from RSS feed.
        """

        # Solution for SSL Error pulled from: https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        parsed_feed = feedparser.parse(self.url)
        return parsed_feed, parsed_feed.keys(), parsed_feed['entries']

    def is_valid_parser(self):
        """
        Determines whether the parsing process was successful.

        Returns:
            bool -- True if parse was successful, false otherwise.
        """

        return ('bozo_exception' not in self.keys) and (self.feed.status == 200)

    def entry(self):
        """Generator function that returns the next entry."""

        for entry in self.entries:
            yield entry

    def _dev_set_entries(self, entries):
        """
        [Development - NOT TO BE USED IN PRODUCTION] Set the entries to a specified list of entries.

        Args:
            entries (list): List of entries to replace self.entries.
        """

        self.entries = entries
