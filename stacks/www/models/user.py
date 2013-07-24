import simplejson
import twitter
from social_auth.db.django_models import UserSocialAuth
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.conf import settings
from stacks.www.models.utils import PropertiesMixin
from stacks.www.utils.cache import get_from_cache, version_key

class Profile(PropertiesMixin, models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "Profile (%s)" % self.user

    class Meta:
        app_label = 'www'

    def is_following(self, followed_user):
        """Returns true if this user is following the given user."""
        return self.user.following.filter(followed_user=followed_user).exists()

    @staticmethod
    def user_saved(sender, instance, **kwargs):
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)

    @staticmethod
    def user_deleted(sender, instance, **kwargs):
        instance.profile.delete()

    def get_twitter_oauth_values(self):
        """Returns the oauth token secret and key for this user."""
        social_auth = UserSocialAuth.objects.get(provider='twitter', user=self.user)
        token_secret, token_key = [t.split('=')[1] for t in social_auth.extra_data['access_token'].split('&')]
        return token_secret, token_key

    def get_twitter_profile(self):
        token_secret, token_key = self.get_twitter_oauth_values()
        api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=token_key,
            access_token_secret=token_secret
        )
        return api.VerifyCredentials().AsDict()

    @property
    def twitter_profile(self):
        """This users's twitter profile: https://dev.twitter.com/docs/api/1/get/account/verify_credentials"""
        if not hasattr(self, '_twitter_profile'):
            self._twitter_profile = simplejson.loads(
                get_from_cache(
                    version_key('twitter_profile', self.user),
                    lambda: simplejson.dumps(self.get_twitter_profile()),
                    60*60*48
                )
            )
        return self._twitter_profile


    # Twitter profile props
    # -------------------------

    @property
    def profile_image_url_24px(self):
        return self.twitter_profile['profile_image_url'].replace('_normal', '_mini')

    @property
    def profile_image_url_48px(self):
        return self.twitter_profile['profile_image_url']

    @property
    def profile_image_url_73px(self):
        return self.twitter_profile['profile_image_url'].replace('_normal', '_bigger')

    @property
    def profile_image_url_original(self):
        return self.twitter_profile['profile_image_url'].replace('_normal', '')

    @property
    def name(self):
        return self.twitter_profile['name']

    @property
    def location(self):
        return self.twitter_profile['location']

    @property
    def description(self):
        return self.twitter_profile['description']

    @property
    def external_url(self):
        return self.twitter_profile['url']

signals.post_save.connect(Profile.user_saved, sender=User)
signals.post_delete.connect(Profile.user_deleted, sender=User)

class Following(PropertiesMixin, models.Model):
    user = models.ForeignKey(User, related_name="following")
    followed_user = models.ForeignKey(User, related_name="followers")
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return "%s follows %s" % (self.user, self.followed_user)

    class Meta:
        app_label = 'www'