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
    image_file = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)
    video_embed = models.TextField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "%s [%s]" % (self.title, MEDIA_ITEM_TYPE_NAME[self.type])

    class Meta:
        app_label = 'www'

    @models.permalink
    def get_absolute_url(self):
        return ('upload_new',) # !! not sure where this is being used

    def save(self, *args, **kwargs):
        self.title = self.image_file
        super(MediaItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image_file.delete(False)
        super(MediaItem, self).delete(*args, **kwargs)