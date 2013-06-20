from django.db import models
from django.contrib.auth.models import User
from stacks.www.models.utils import PropertiesMixin, CacheMixin
from stacks.www.models.site import Site
from stacks.www.utils.cache import incr_version, version_key, get_from_cache, safe_cache_key

class Page(PropertiesMixin, CacheMixin, models.Model):
    user = models.ForeignKey(User, related_name="pages")
    site = models.ForeignKey(Site, related_name="pages")
    title = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    layout = models.ForeignKey("Layout", related_name="pages")
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'www'
        unique_together = (("slug", "site"),)

    def invalidate_cache(self):
        # invalidate collections and individual by ID and by slug + site
        incr_version('pages')
        incr_version('page-id-' + str(self.id))
        incr_version(safe_cache_key('page-slug-' + self.slug + '.' + 'page-site-' + self.site_id))

    @classmethod
    def get_from_cache(cls, id=None, site=None, slug=None):
        assert id or (site and slug), "Must supply either an ID or a site and a slug"

        if id:
            return get_from_cache(
                version_key('page-id-' + str(id)),
                lambda: cls.objects.get(id=id))
        elif site and slug:
            return get_from_cache(
                version_key(safe_cache_key('page-slug-' + slug + '.' + 'page-site-' + str(site.id))),
                lambda: cls.objects.get(site=site, slug=slug))

class PageMediaItem(models.Model):
    page = models.ForeignKey("Page", related_name="items")
    placement = models.CharField(max_length=64, db_index=True)
    item = models.ForeignKey("MediaItem", related_name="pages")

    def __unicode__(self):
        return '%s for %s' % (self.placement, self.page)

    class Meta:
        app_label = 'www'