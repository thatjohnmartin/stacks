from django.db import models
from django.conf import settings
from stacks.www.models.utils import PropertiesMixin, CacheMixin
from stacks.www.utils.cache import incr_version, version_key, get_from_cache
from stacks import constants

class Site(PropertiesMixin, CacheMixin, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(max_length=255, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'www'

    def invalidate_cache(self):
        # invalidate collections and individual by ID
        incr_version('sites')
        incr_version('site-id-' + str(self.id))
        incr_version('site-short-name-' + self.short_name)

    @classmethod
    def get_from_cache(cls, id=None, short_name=None):
        assert id != None or short_name, "Must supply either an ID or a short name"

        if id:
            return get_from_cache(
                version_key('site-id-' + str(id)),
                lambda: cls.objects.get(id=id))
        elif short_name:
            return get_from_cache(
                version_key('site-short-name-' + short_name),
                lambda: cls.objects.get(short_name=short_name))

    @property
    def is_home(self):
        return self.id == constants.HOME_SITE_ID

    @property
    def is_astro(self):
        return self.id == constants.ASTRO_SITE_ID

    @property
    def is_climbing(self):
        return self.id == constants.CLIMBING_SITE_ID
