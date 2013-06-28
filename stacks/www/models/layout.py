from django.db import models
from stacks.www.models.utils import PropertiesMixin

class Layout(PropertiesMixin, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    site = models.ForeignKey("Site", null=True, blank=True, related_name="site_specific_stacks")
    description = models.TextField(blank=True)
    template_file = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    template_source = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'www'