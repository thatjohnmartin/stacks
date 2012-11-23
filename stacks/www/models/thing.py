from django.db import models
from stacks.www.models.utils import PropertiesMixin, AutoSlugMixin

# - movie
#     - series
# - tv show
#     - season
#     - episode
# - book
#     - series
# - universe

#THING_TYPE_MOVIE = 10
#THING_TYPE_TV_SHOW = 20
#THING_TYPE_BOOK = 30
#THING_TYPE_UNIVERSE = 100
#
#THING_TYPE_CHOICES = (
#    (THING_TYPE_MOVIE, 'Movie'),
#    (THING_TYPE_TV_SHOW, 'TV Show'),
#    (THING_TYPE_BOOK, 'Book'),
#    (THING_TYPE_UNIVERSE, 'Universe'))
#
#THING_TYPE_NAME = dict((s, n.lower()) for s, n in THING_TYPE_CHOICES)
#
#class Thing(AutoSlugMixin, PropertiesMixin, models.Model):
#    title = models.CharField(max_length=200)
#    type = models.IntegerField(choices=THING_TYPE_CHOICES, db_index=True)
#    published = models.DateTimeField(null=True, blank=True, db_index=True) # the date the item was published e.g. air date
#    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
#    modified = models.DateTimeField(auto_now=True, db_index=True)
#
#    def __unicode__(self):
#        return self.title
#
#    class Meta:
#        app_label = 'www'