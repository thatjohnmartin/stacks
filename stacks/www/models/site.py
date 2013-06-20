from django.db import models
from django.conf import settings
from stacks.www.models.utils import PropertiesMixin, CacheMixin
from stacks.www.utils.cache import incr_version, version_key, get_from_cache

ASTRO_SITE_ID = 1
CLIMBING_SITE_ID = 2

class Site(PropertiesMixin, CacheMixin, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(max_length=255, db_index=True)
    domain_local = models.CharField(max_length=255, db_index=True)
    domain_prod = models.CharField(max_length=255, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'www'

    def invalidate_cache(self):
        # invalidate collections and individual by ID
        incr_version('sites')
        incr_version('site-id-' + str(self.id))

    @classmethod
    def get_from_cache(cls, id=None, domain=None):
        assert id or domain, "Must supply either an ID or a domain"

        if id:
            return get_from_cache(
                version_key('site-id-' + str(id)),
                lambda: cls.objects.get(id=id))
        elif domain:
            if settings.IS_LOCAL:
                return get_from_cache(
                    version_key('site-domain-local-' + domain),
                    lambda: cls.objects.get(domain_local=domain))
            else:
                return get_from_cache(
                    version_key('site-domain-prod-' + domain),
                    lambda: cls.objects.get(domain_prod=domain))

    @property
    def domain(self):
        "Returns the appropriate domain based on current settings, local or prod."
        return self.domain_local if settings.IS_LOCAL else self.domain_prod

    @property
    def is_astro(self):
        return self.id == ASTRO_SITE_ID

    @property
    def is_climbing(self):
        return self.id == CLIMBING_SITE_ID
