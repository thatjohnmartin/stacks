from collections import defaultdict
from django.conf import settings
from stacks.www.utils.cache import safe_cache_key, get_from_cache

_SCRAPERS = defaultdict(dict)

def scrape(provider, resource, url):
    """Scrapes a resource at the provider with the URL, or pulls it from the cache."""
    if settings.ENABLE_SCRAPER_CACHE:
        return get_from_cache(
            safe_cache_key('scraper-%s-%s-%s' % (provider, resource, url)),
            lambda: _SCRAPERS[provider][resource](url),
            ttl=60*60*24*7 # a week
        )
    else:
        return _SCRAPERS[provider][resource](url)

import mountain_project
import simbad
import super_topo
import wikipedia
