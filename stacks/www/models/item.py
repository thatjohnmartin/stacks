from crimpycache.models import CacheMixin
from django.db import models
from django.contrib.auth.models import User

class Item(CacheMixin, models.Model):
    user = models.ForeignKey(User, null=True, blank=True, related_name="library_items")
    path = models.CharField(max_length=255, db_index=True)
    value = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.full_path

    class Meta:
        app_label = 'www'
        unique_together = (("user", "path"),)

    @property
    def full_path(self):
        if self.user:
            return 'library.users.%s.%s' % (self.user, self.path)
        else:
            return 'library.globals.%s' % self.path