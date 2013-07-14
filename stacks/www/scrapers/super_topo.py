from stacks.www.scrapers.decorators import scraper

@scraper('super_topo', 'x-route-topo-json')
def super_topo_route(url):
    return {}

@scraper('super_topo', 'x-area-topo-json')
def super_topo_area(url):
    return {}
