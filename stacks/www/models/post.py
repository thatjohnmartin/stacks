from django.db import models
from stacks.www.models.utils import PropertiesMixin, AutoSlugMixin

POST_TYPE_LINK = 10
POST_TYPE_ARTICLE = 20
POST_TYPE_VIDEO = 30

POST_TYPE_CHOICES = (
    (POST_TYPE_LINK, 'Link'),
    (POST_TYPE_ARTICLE, 'Article'),
    (POST_TYPE_VIDEO, 'Video'),
)

POST_TYPE_NAME = dict((s, n.lower()) for s, n in POST_TYPE_CHOICES)

class Post(AutoSlugMixin, PropertiesMixin, models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    thing = models.ForeignKey('Thing', related_name="posts")
    type = models.IntegerField(choices=POST_TYPE_CHOICES, db_index=True)
    content = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=1024, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'www'
