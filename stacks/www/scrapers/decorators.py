from stacks.www.scrapers import _SCRAPERS

def scraper(provider, resource):
    """Decorator to add scrapers to the SCRAPERS dict."""
    def wrap(scraper_function):
        def wrapped_scraper(url):
            scraper_function(scraper_function)
        _SCRAPERS[provider][resource] = scraper_function
        return wrapped_scraper
    return wrap
