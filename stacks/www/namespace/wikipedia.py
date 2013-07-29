from stacks.www.namespace import NameSpace, VirtualSubspace, ReadOnlyNameSpace
from stacks.www.scrapers import scrape

API_URL = 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content'
PAGE_URL = 'http://en.wikipedia.org/wiki/%s'

class WikipediaItem(object):
    pass

class WikipediaAstroObject(WikipediaItem):
    """A lazy-loaded Wikipedia astro object."""

    def __init__(self, wiki_name):
        self._loaded = False
        self._wiki_name = wiki_name

    def _load(self):
        self._internal_astro_object = scrape('wikipedia', 'x-astro-object-json', API_URL % self._wiki_name)

    @property
    def _astro_object(self):
        if not self._loaded:
            self._load()
        return self._internal_astro_object

    def __repr__(self):
        return "<WikipediaAstroObject: %s (not loaded)>" % self._wiki_name

    @property
    def wiki_name(self):
        return self._wiki_name

    @property
    def wikipedia_page_url(self):
        return PAGE_URL % self._wiki_name

    @property
    def name(self):
        return self._astro_object['name']

    @property
    def type(self):
        return self._astro_object['type']

    @property
    def constellation(self):
        return self._astro_object['constellation']

    @property
    def radius_ly(self):
        return self._astro_object['radius_ly']

class WikipediaNameSpace(ReadOnlyNameSpace):
    """A namespace of Flickr-y things: photos, sets. Configured for a single Flickr user account."""

    def __init__(self):
        super(NameSpace, self).__setitem__('astro_objects', WikipediaAstroObjectsSubspace())
        super(NameSpace, self).__setitem__('mountains', WikipediaMountainsSubspace())
        super(WikipediaNameSpace, self).__init__(subspace_name='wikipedia')

class WikipediaAstroObjectsSubspace(VirtualSubspace):
    """A virtual subspace of lazy-loaded Wikipedia astro objects."""

    def __init__(self):
        super(NameSpace, self).__setattr__('_loaded', False)
        super(WikipediaAstroObjectsSubspace, self).__init__(subspace_name='astro_objects', structured=False)

    def __repr__(self):
        if self._loaded:
            return repr(self._internal_astro_objects)
        else:
            return "{<not loaded>}"

    def _load(self):
        # faked list for now
        wiki_names = ['Boomerang_Nebula', 'Fox_Fur_Nebula', 'Pelican_Nebula', 'Rosette_Nebula']

        astro_objects_dict = {}
        for name in wiki_names:
            astro_objects_dict[name] = WikipediaAstroObject(name)

        super(NameSpace, self).__setattr__('_internal_astro_objects', astro_objects_dict)
        super(NameSpace, self).__setattr__('_loaded', True)

    @property
    def _astro_objects(self):
        if not self._loaded:
            self._load()
        return self._internal_astro_objects

    def __iter__(self):
        for k in self._astro_objects:
            yield k

    def keys(self):
        return self._astro_objects.keys()

    def __contains__(self, key):
        return key in self._astro_objects

    def __len__(self):
        return len(self._astro_objects)

    def __getitem__(self, key):
        if key not in self._astro_objects:
            return KeyError(key)
        return self._astro_objects[key]

class WikipediaMountainsSubspace(VirtualSubspace):
    """A virtual subspace of lazy-loaded Wikipedia mountains."""

    def __init__(self):
        super(NameSpace, self).__setattr__('_loaded', False)
        super(WikipediaMountainsSubspace, self).__init__(subspace_name='mountains', structured=False)

    def __repr__(self):
        return "{<not loaded>}"
