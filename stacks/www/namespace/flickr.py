import flickrapi
from django.conf import settings
from stacks.www.namespace import NameSpace

class FlickrNameSpace(NameSpace):

    def __init__(self, subspace_name=''):
        pass

    def __getitem__(self, key):
        if key == "photos":
            return {'8787002065': LazyFlickrPhoto('8787002065'), '8711102065': LazyFlickrPhoto('8711102065')}
        else:
            raise AttributeError(key)

    # make it read-only
    def __setitem__(self, key, val):
        raise Exception('Not writeable!')

class FlickrPhoto(object):

    def __init__(self, photo_id):
        self.loaded = False
        self.photo_id = photo_id

    def _load(self):
        flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, format='json')
        flickr.people_getPublicPhotos(user_id='67298421@N00')

    def __repr__(self):
        return "<LazyFlickrPhoto: %s>" % self.photo_id

    def __unicode__(self):
        return "<LazyFlickrPhoto: %s>" % self.photo_id

    @property
    def url(self):
        return "www.foo.com"