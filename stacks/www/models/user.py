from django.db import models
from django.contrib.auth.models import User
from stacks.www.models.utils import PropertiesMixin

class Profile(PropertiesMixin, models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "Profile (%s)" % self.user

    class Meta:
        app_label = 'www'

    def is_following(self, followed_user):
        """Returns true if this user is following the given user."""
        return self.user.following.filter(followed_user=followed_user).exists()

class Following(PropertiesMixin, models.Model):
    user = models.ForeignKey(User, related_name="following")
    followed_user = models.ForeignKey(User, related_name="followers")
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return "%s follows %s" % (self.user, self.followed_user)

    class Meta:
        app_label = 'www'