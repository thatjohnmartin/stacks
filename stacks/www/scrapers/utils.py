import urllib2
import datetime

def build_opener():
    """Builds an opener with a useful user agent."""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1')]
    return opener

def add_scrape_metadata(context, url, date=None):
    """Adds scrape metadata to the given context dict."""
    if not date:
        date = datetime.datetime.now()
    context['_scrape'] = {'url': url, 'date': date }
