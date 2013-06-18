from django.db import models
from django.contrib.auth.models import User
from stacks.www.models.utils import PropertiesMixin
from stacks.www.models.site import Site

class Page(PropertiesMixin, models.Model):
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

class PageMediaItem(models.Model):
    page = models.ForeignKey("Page", related_name="items")
    placement = models.CharField(max_length=64, db_index=True)
    item = models.ForeignKey("MediaItem", related_name="pages")

    def __unicode__(self):
        return '%s for %s' % (self.placement, self.page)

    class Meta:
        app_label = 'www'