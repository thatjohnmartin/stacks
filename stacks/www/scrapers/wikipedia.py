import re
import simplejson
from stacks.www.scrapers.decorators import scraper
from stacks.www.scrapers.utils import build_opener, add_scrape_metadata

page_query = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content"

def _parse_page(page_json):
    """Digs into a wikipedia JSON response, grabs the page content, then splits it into infobox and body."""
    pages = page_json['query']['pages']
    wikitext = pages[pages.keys()[0]]['revisions'][0]['*']

    splitter = '}}\n\n'
    end_of_infobox = wikitext.find(splitter) # assume the first '}}\n\n' is the end
    infobox = wikitext[:end_of_infobox]
    body = wikitext[end_of_infobox + len(splitter):]
    return infobox, body

info_box_value_re_string = "\|\s*%s\s*=\s*(.*?)\n"
wikilink_text_re = re.compile(r"\[\[(.*\|)?(.*)\]\]")

def _get_infobox_value(infobox_text, value_name):
    """Pulls out a named value in an infobox. Flattens any wiki links to plain text."""
    value = ""
    value_re = re.compile(info_box_value_re_string % value_name.lower())
    m = value_re.search(infobox_text)
    if m:
        value = m.groups()[0]

        # check for a wiki link
        if value.startswith('[['):
            m2 = wikilink_text_re.search(value)
            if m2:
                value = m2.groups()[1]

    return value

@scraper('wikipedia', 'x-astro-object-json')
def wikipedia_astro_object(url):
    """Scrapes an astro object page on wikipedia."""

    opener = build_opener()
    infobox, body = _parse_page(simplejson.loads(opener.open(url).read()))

    astro = {
        'name': _get_infobox_value(infobox, 'name'),
        'type': _get_infobox_value(infobox, 'type'),
        'constellation': _get_infobox_value(infobox, 'constellation'),
        'radius_ly': _get_infobox_value(infobox, 'radius_ly'),
    }

    add_scrape_metadata(astro, url)

    return astro