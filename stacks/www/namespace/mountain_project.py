from stacks.www.namespace import NameSpace, VirtualSubspace, ReadOnlyNameSpace
from stacks.www.scrapers import scrape

API_URL = PAGE_URL = 'http://www.mountainproject.com/v/%s' # e.g. 'the-links-effect/108174183'

class MountainProjectItem(object):
    pass

class MountainProjectRoute(MountainProjectItem):
    """A lazy-loaded Mountain Project route."""

    def __init__(self, route_id):
        self._loaded = False
        self._route_id = route_id

    def _load(self):
        self._internal_route = scrape('mountain_project', 'x-route-topo-json', API_URL % self._route_id)

    @property
    def _route(self):
        if not self._loaded:
            self._load()
        return self._internal_route

    def __repr__(self):
        return "<MountainProjectRoute: %s (not loaded)>" % self._route_id

    @property
    def route_id(self):
        return self._route_id

    @property
    def mountain_project_page_url(self):
        return PAGE_URL % self._route_id

    @property
    def name(self):
        return self._route['name']

    @property
    def location_name(self):
        return self._route['location']['name']

    @property
    def location_url(self):
        return self._route['location']['url']

    @property
    def area_name(self):
        return self._route['area']['name']

    @property
    def area_url(self):
        return self._route['area']['url']

    @property
    def grade(self):
        return self._route['grade']

    @property
    def type(self):
        return self._route['type']

    @property
    def consensus(self):
        return self._route['consensus']

    @property
    def fa(self):
        return self._route['fa']

class MountainProjectNameSpace(ReadOnlyNameSpace):
    """A namespace of Flickr-y things: photos, sets. Configured for a single Flickr user account."""

    def __init__(self):
        super(NameSpace, self).__setitem__('routes', MountainProjectRoutesSubspace())
        super(NameSpace, self).__setitem__('areas', MountainProjectAreasSubspace())
        super(MountainProjectNameSpace, self).__init__(subspace_name='mountain_project')

class MountainProjectRoutesSubspace(VirtualSubspace):
    """A virtual subspace of lazy-loaded MountainProject astro objects."""

    def __init__(self):
        super(NameSpace, self).__setattr__('_loaded', False)
        super(MountainProjectRoutesSubspace, self).__init__(subspace_name='routes', structured=False)

    def __repr__(self):
        if self._loaded:
            return repr(self._internal_astro_objects)
        else:
            return "{<not loaded>}"

    def _load(self):
        # faked list for now
        route_ids = [
            'the-links-effect/108174183',
            'post-orgasmic-depression/105952181',
            'sport-climbing-is-neither/105732554',
            'under-the-boardwalk/105813238'
        ]

        routes_dict = {}
        for id in route_ids:
            routes_dict[id] = MountainProjectRoute(id)

        super(NameSpace, self).__setattr__('_internal_routes', routes_dict)
        super(NameSpace, self).__setattr__('_loaded', True)

    @property
    def _routes(self):
        if not self._loaded:
            self._load()
        return self._internal_routes

    def __iter__(self):
        for k in self._routes:
            yield k

    def keys(self):
        return self._routes.keys()

    def __contains__(self, key):
        return key in self._routes

    def __len__(self):
        return len(self._routes)

    def __getitem__(self, key):
        if key not in self._routes:
            return KeyError(key)
        return self._routes[key]

class MountainProjectAreasSubspace(VirtualSubspace):
    """A virtual subspace of lazy-loaded MountainProject mountains."""

    def __init__(self):
        super(NameSpace, self).__setattr__('_loaded', False)
        super(MountainProjectAreasSubspace, self).__init__(subspace_name='areas', structured=False)

    def __repr__(self):
        return "{<not loaded>}"
