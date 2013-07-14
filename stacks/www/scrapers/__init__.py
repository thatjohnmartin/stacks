from collections import defaultdict
from stacks.www.utils.cache import safe_cache_key, get_from_cache

_SCRAPERS = defaultdict(dict)

def scrape(provider, resource, url):
    """Scrapes a resource at the provider with the URL, or pulls it from the cache."""
    return get_from_cache(
        safe_cache_key('scraper-%s-%s-%s' % (provider, resource, url)),
        lambda: _SCRAPERS[provider][resource](url),
        ttl=60*60*24*7 # a week
    )