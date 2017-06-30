import feedparser
import time


class NewFeed:
    """ Class for parsing RSS Feed.
    We need just title, link and published date
    """

    def __init__(self):
        self._links = {
            'job': 'https://www.djangoproject.com/rss/community/jobs/',
            'blog': 'https://www.djangoproject.com/rss/community/blogs/',
            'link': 'https://www.djangoproject.com/rss/community/links/'
        }

    def get_news(self, start_from):
        result = []
        for link in self._links:
            feed = feedparser.parse(self._links[link])
            for f in feed['entries']:
                if start_from < int(time.mktime(f['published_parsed'])):
                    result.append(
                        (
                            f['title'][:75],
                            f['link'],
                            link,
                            int(time.mktime(f['published_parsed']))
                        )
                    )
        return result
