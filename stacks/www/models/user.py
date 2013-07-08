from django.db import models
from django.contrib.auth.models import User
from stacks.www.models.utils import PropertiesMixin

class Profile(PropertiesMixin, models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "Profile (%s)" % self.user

    class Meta:
        app_label = 'www'

class Following(PropertiesMixin, models.Model):
    user = models.ForeignKey(User, related_name="following")
    followed_user = models.ForeignKey(User, related_name="followers")
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return "%s follows %s" % (self.user, self.followed_user)

    class Meta:
        app_label = 'www'