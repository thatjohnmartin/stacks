from stacks.www.scrapers.decorators import scraper

@scraper('simbad', 'x-astro-object-json')
def simbad_object_page(url):
    """Scrapes a SIMBAD query result (or object) page."""
    return {}