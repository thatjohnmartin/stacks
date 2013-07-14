import urllib2
import datetime
import re
from bs4 import BeautifulSoup
from stacks.www.scrapers.decorators import scraper

@scraper('wikipedia', 'x-astro-object-json')
def wikipedia_astro_object_page(url):
    """Scrapes an astro object page on wikipedia."""

    astro = {}

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    soup = BeautifulSoup(urllib2.urlopen(url), 'lxml')

    h1 = soup.find('h1', class_="firstHeading")
    astro['name'] = h1.text.strip()

    def _get_value_in_td(text):
        th = soup.find('th', scope="row", text=text)
        if th:
            td = th.next_sibling
            if td:
                return td.text
        return ''

    astro['type'] = _get_value_in_td(re.compile('^Type'))
    astro['distance'] = _get_value_in_td(re.compile('^Distance'))
    astro['Constellation'] = _get_value_in_td(re.compile('^Constellation'))
    astro['Radius'] = _get_value_in_td(re.compile('^Radius'))

    # update scraping metadata
    astro['_scrape'] = {'url': url, 'date': datetime.datetime.now()}

    return astro