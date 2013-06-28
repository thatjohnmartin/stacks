from django.db import models
from stacks.www.models.utils import PropertiesMixin, CacheMixin
from stacks.www.models import Stack, Layout
from stacks.www.utils.cache import incr_version, version_key, get_from_cache, safe_cache_key

class Block(PropertiesMixin, CacheMixin, models.Model):
    stack = models.ForeignKey(Stack, related_name="blocks")
    name = models.CharField(max_length=255, db_index=True)
    layout = models.ForeignKey(Layout, related_name="blocks")
    order = models.IntegerField(default=0, null=False, db_index=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'www'
        unique_together = (("stack", "name"),)

    def invalidate_cache(self):
        # invalidate collections and individual by ID and by slug + site
        incr_version('blocks')
        incr_version('block-id-' + str(self.id))

    @classmethod
    def get_from_cache(cls, id):
        return get_from_cache(
            version_key('block-id-' + str(id)),
            lambda: cls.objects.get(id=id))

# keeping this just for future reference...
#
# class PageMediaItem(models.Model):
#     page = models.ForeignKey("Page", related_name="items")
#     placement = models.CharField(max_length=64, db_index=True)
#     item = models.ForeignKey("MediaItem", related_name="pages")
#
#     def __unicode__(self):
#         return '%s for %s' % (self.placement, self.page)
#
#     class Meta:
#         app_label = 'www'