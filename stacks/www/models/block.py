from crimpycache.models import CacheMixin
from django.db import models
from stacks.www.models.utils import PropertiesMixin
from stacks.www.models import Stack, Layout

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

    # def invalidate_cache(self):
    #     # invalidate collections and individual by ID and by slug + site
    #     incr_version('blocks')
    #     incr_version('block-id-' + str(self.id))
    #
    # @classmethod
    # def get_from_cache(cls, id):
    #     return get_from_cache(
    #         version_key('block-id-' + str(id)),
    #         lambda: cls.objects.get(id=id))

# example items in block.properties.context
#
#   "image1": {
#     "type": "image/jpeg",
#     "provider": "path",
#     "value": "users.johnm.library.flickr.image.8787002065"
#   },
#   "image2": {
#     "type": "image/jpeg",
#     "provider": "url",
#     "value": "http://farm8.staticflickr.com/7291/8787002065_0813f26e5f_c.jpg"
#   },
#   "image3": {
#     "type": "image/jpeg",
#     "provider": "flickr",
#     "value": "8787002065"
#   },
#   "gear1": {
#     "type": "application/json",
#     "value": {"manufacturer": "Losmandy", "model": "210c", "capacity": 45}
#   }
#   "gear2": {
#     "type": "application/json",
#     "provider": "path",
#     "value": "global.library.json.gear.losmandy_210c"
#   },
#   "gear3": {
#     "type": "application/json",
#     "provider": "url",
#     "value": "http://astrodb.com/gear/mounts/losmandy_210c.json"
#   },
#   "stats1": {
#     "type": "text/csv",
#     "value": "Item,Value|Scope,Losmandy|Foo,12.5"
#   },
#   "text1": {
#     "type": "text/html",
#     "value": "<p>This is some HTML.</p>"
#   },
#   "text2": {
#     "type": "text/x-markdown",
#     "value": "This is *some* markdown."
#   },
#   "text3": {
#     "type": "text/plain",
#     "value": "This is just plain old text."
#   },
#
# supported (mime)types: image, text/html, text/x-markdown, text/plain, application/json, text/csv
# supported providers: inline (default), path, url, flickr
#
# Notes:
#
#   * subtypes are required in items, but not in placeholders


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