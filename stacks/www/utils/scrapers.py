import urllib2
import datetime
import re
from bs4 import BeautifulSoup

def mountain_project_climb_page(url):
    """Scrapes a regular climb page."""

    climb = {}

    soup = BeautifulSoup(urllib2.urlopen(url), 'lxml')

    h1 = soup.find('h1', class_="dkorange")
    climb['name'] = h1.text.strip()
    climb['grade'] = h1.next_sibling.text

    location_links = soup.find('div', id='navBox').findChildren('a')[1:] # ignore the "all locations" link
    first_link = location_links.pop(0)
    if first_link.text == 'International': # ignore the international link
        first_link = location_links.pop(0)

    climb['location'] = {"name": first_link.text, "url": first_link['href']}
    climb['area'] = [{'name': a.text, 'url': a['href']} for a in location_links]

    def _get_value_in_td(text):
        td = soup.find('td', text=text)
        if td:
            next_td = td.next_sibling
            if next_td:
                return next_td.text
        return ''

    climb['type'] = _get_value_in_td(re.compile('^Type'))
    climb['consensus'] = _get_value_in_td(re.compile('^Consensus'))
    climb['fa'] = _get_value_in_td(re.compile('^FA'))
    climb['url'] = url

    # update scraping metadata
    climb['_scrape'] = {'url': url, 'date': datetime.datetime.now()}

    return climb