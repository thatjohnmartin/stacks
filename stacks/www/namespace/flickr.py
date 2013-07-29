from dateutil import parser
from datetime import datetime
import flickrapi
from stacks.www.namespace import NameSpace, VirtualSubspace, ReadOnlyNameSpace

class FlickrPhoto(object):
    """A lazy-loaded Flickr photo."""

    def __init__(self, flickr_api_key, photo_id):
        self._loaded = False
        self._flickr_api_key = flickr_api_key
        self._photo_id = photo_id

    def _load(self):
        flickr = flickrapi.FlickrAPI(self._flickr_api_key)
        p = {}

        # get some basic photo info
        response = flickr.photos_getInfo(photo_id=self._photo_id)
        photo = response.find('photo')
        p['media'] = photo.attrib['media']
        p['title'] = photo.find('title').text
        p['flickr_page_url'] = photo.find('urls').find('url').text
        dates = photo.find('dates')
        p['date_taken'] = parser.parse(dates.attrib['taken'])
        p['date_added'] = datetime.fromtimestamp(int(dates.attrib['posted']))

        # get URLs to the various image sizes
        response = flickr.photos_getSizes(photo_id=self._photo_id)
        for size in response.find('sizes').findall('size'):
            if size.attrib['label'] == 'Original':
                name = 'original'
            else:
                name = 'url_%sx%s' % (size.attrib['width'], size.attrib['height'])
            p[name] = size.attrib['source']
        self._internal_photo = p

    @property
    def _photo(self):
        if not self._loaded:
            self._load()
        return self._internal_photo

    def __repr__(self):
        return "<FlickrPhoto: %s (not loaded)>" % self._photo_id

    @property
    def media_type(self):
        """Returns 'photo' or 'video'."""
        return self._photo['media']

    def is_photo(self):
        return self._photo['media'] == 'photo'

    def is_video(self):
        return self._photo['media'] == 'video'

    @property
    def title(self):
        return self._photo['title']

    @property
    def flickr_page_url(self):
        return self._photo['flickr_page_url']

    @property
    def id(self):
        return self._photo_id

    @property
    def url_75x75(self):
        return self._photo['url_75x75']

    @property
    def url_150x150(self):
        return self._photo['url_150x150']

    @property
    def url_320x240(self):
        return self._photo['url_320x240']

    @property
    def url_500x375(self):
        return self._photo['url_500x375']

    @property
    def url_640x480(self):
        return self._photo['url_640x480']

    @property
    def url_800x600(self):
        return self._photo['url_800x600']

    @property
    def url_1024x768(self):
        return self._photo['url_1024x768']

    @property
    def url_1600x1200(self):
        return self._photo['url_1600x1200']

    @property
    def url_original(self):
        return self._photo['url_original']

    @property
    def date_taken(self):
        return self._photo['date_taken']

    @property
    def date_added(self):
        return self._photo['date_added']

class FlickrNameSpace(ReadOnlyNameSpace):
    """A namespace of Flickr-y things: photos, sets. Configured for a single Flickr user account."""

    def __init__(self, flickr_api_key, flickr_username):
        super(NameSpace, self).__setattr__('_flickr_api_key', flickr_api_key)
        super(NameSpace, self).__setattr__('_flickr_username', flickr_username)
        super(NameSpace, self).__setitem__('photos', FlickrPhotosSubspace(flickr_api_key, flickr_username))
        super(NameSpace, self).__setitem__('sets', FlickrSetsSubspace(flickr_api_key, flickr_username))
        super(FlickrNameSpace, self).__init__(subspace_name='flickr')

class FlickrPhotosSubspace(VirtualSubspace):
    """A virtual subspace of lazy-loaded Flickr photos."""

    def __init__(self, flickr_api_key, flickr_username):
        super(NameSpace, self).__setattr__('_flickr_api_key', flickr_api_key)
        super(NameSpace, self).__setattr__('_flickr_username', flickr_username)
        super(NameSpace, self).__setattr__('_loaded', False)
        super(FlickrPhotosSubspace, self).__init__(subspace_name='photos', structured=False)

    def __repr__(self):
        if self._loaded:
            return repr(self._photos)
        else:
            return "{<not loaded>}"

    def _load(self):
        flickr = flickrapi.FlickrAPI(self._flickr_api_key)

        photos_dict = {}
        for page in range(1, 100):
            # BTW, 100 is an arbitrary maximum .. not sure how big some people's Flickr accounts will be
            response = flickr.people_getPublicPhotos(user_id=self._flickr_username, per_page=100, page=page)
            photos = response.find('photos')
            for id in [photo.attrib['id'] for photo in photos.findall('photo')]:
                photos_dict[id] = FlickrPhoto(self._flickr_api_key, id)
            if page >= int(photos.attrib['pages']):
                break

        super(NameSpace, self).__setattr__('_internal_photos', photos_dict)
        super(NameSpace, self).__setattr__('_loaded', True)

    @property
    def _photos(self):
        if not self._loaded:
            self._load()
        return self._internal_photos

    def __iter__(self):
        for k in self._photos:
            yield k

    def keys(self):
        return self._photos.keys()

    def __contains__(self, key):
        return key in self._photos

    def __len__(self):
        return len(self._photos)

    def __getitem__(self, key):
        if key not in self._photos:
            return KeyError(key)
        return self._photos[key]

class FlickrSetsSubspace(VirtualSubspace):
    """A virtual subspace of lazy-loaded Flickr sets."""

    def __init__(self, flickr_api_key, flickr_username):
        super(NameSpace, self).__setattr__('_flickr_api_key', flickr_api_key)
        super(NameSpace, self).__setattr__('_flickr_username', flickr_username)
        super(NameSpace, self).__setattr__('_loaded', False)
        super(FlickrSetsSubspace, self).__init__(subspace_name='sets', structured=False)
