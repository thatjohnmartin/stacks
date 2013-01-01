from django.db import models
from django.contrib.auth.models import User
from stacks.www.models.utils import PropertiesMixin

MEDIA_ITEM_TYPE_IMAGE = 10
MEDIA_ITEM_TYPE_VIDEO = 20

MEDIA_ITEM_TYPE_CHOICES = (
    (MEDIA_ITEM_TYPE_IMAGE, 'Image'),
    (MEDIA_ITEM_TYPE_VIDEO, 'Video'),
)

MEDIA_ITEM_TYPE_NAME = dict((s, n.lower()) for s, n in MEDIA_ITEM_TYPE_CHOICES)

# !! intended to support both images and videos, but right now only coded for images

class MediaItem(PropertiesMixin, models.Model):
    user = models.ForeignKey(User, related_name="items")
    title = models.CharField(max_length=255, null=True, blank=True)
    type = models.IntegerField(choices=MEDIA_ITEM_TYPE_CHOICES, default=MEDIA_ITEM_TYPE_IMAGE, db_index=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    video_embed = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "%s [%s]" % (self.title, MEDIA_ITEM_TYPE_NAME[self.type])

    class Meta:
        app_label = 'www'