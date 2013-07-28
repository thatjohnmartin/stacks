import flickrapi
from stacks.www.namespace import NameSpace, VirtualSubspace

class FlickrNameSpace(VirtualSubspace):

    def __init__(self, flickr_api_key, flickr_username):
        super(NameSpace, self).__setattr__('_flickr_api_key',  flickr_api_key)
        super(NameSpace, self).__setattr__('_flickr_username',  flickr_username)
        super(FlickrNameSpace, self).__init__('flickr', structured=False)

    def __getitem__(self, key):
        if key == "photos":
            return {
                '8787002065': FlickrPhoto(self._flickr_api_key, '8787002065'),
                '8711102065': FlickrPhoto(self._flickr_api_key, '8711102065')
            }
        else:
            raise AttributeError(key)

class FlickrPhoto(object):

    def __init__(self, flickr_api_key, photo_id):
        self._loaded = False
        self._flickr_api_key = flickr_api_key
        self._photo_id = photo_id

    def _load(self):
        flickr = flickrapi.FlickrAPI(self._flickr_api_key, format='json')
        flickr.people_getPublicPhotos(user_id='67298421@N00')

    def __repr__(self):
        return "<FlickrPhoto: %s>" % self._photo_id

    def __unicode__(self):
        return "<FlickrPhoto: %s>" % self._photo_id

    @property
    def url(self):
        return "www.foo.com"