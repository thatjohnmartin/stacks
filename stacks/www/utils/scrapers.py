import urllib2
import datetime
from bs4 import BeautifulSoup

class BaseScraper():
    def update_item(self, item):
        pass

class MountainProjectScraper(BaseScraper):
    def update_item(self, item):
        if '_scrape' not in item:
            # what to do here??
            pass

        # only update if empty, not based on date expiration (yet)
        if not item['_scrape']['date']:
            soup = BeautifulSoup(urllib2.urlopen(item['_scrape']['url']))

            type_label = soup.find('td', text='Type:')



            item['url'] = item['_scrape']['url']
            item['type'] = "Sport, Foo"
            item['grade'] = "5.9R"
            item['fa'] = "John Martin, 1994"

            item['_scrape']['date'] = datetime.datetime.now()