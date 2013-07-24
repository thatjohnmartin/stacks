from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from stacks.www.models.utils import PropertiesMixin, CacheMixin
from stacks.www.utils.cache import incr_version, version_key, get_from_cache, safe_cache_key

class Stack(PropertiesMixin, CacheMixin, models.Model):
    user = models.ForeignKey(User, related_name="stacks")
    site = models.ForeignKey("Site", related_name="stacks")
    title = models.CharField(max_length=255, db_index=True)
    subtitle = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'www'
        unique_together = (("slug", "site"),)

    def invalidate_cache(self):
        # invalidate collections and individual by ID and by slug + site
        incr_version('stacks')
        incr_version('stack-id-' + str(self.id))
        incr_version(safe_cache_key('stack-slug-' + self.slug + '.' + 'stack-site-' + self.site_id))

    @classmethod
    def get_from_cache(cls, id=None, site=None, slug=None):
        assert id or (site and slug), "Must supply either an ID or a site and a slug"

        if id:
            return get_from_cache(
                version_key('stack-id-' + str(id)),
                lambda: cls.objects.get(id=id))
        elif site and slug:
            return get_from_cache(
                version_key(safe_cache_key('stack-slug-' + slug + '.' + 'stack-site-' + str(site.id))),
                lambda: cls.objects.get(site=site, slug=slug))

    @property
    def like_count(self):
        """Returns the number of likes for this stack."""
        return get_from_cache(
            version_key('stack-likes-' + str(self.id)) + '.like-count',
            lambda: self.likes.count())

    @property
    def liked_by(self):
        """Returns a list of users that have liked this stack."""
        return get_from_cache(
            version_key('stack-likes-' + str(self.id)) + '.liked-by',
            lambda: [like.user for like in self.likes.only("user")])

    def liked_by_user(self, user):
        """Returns true if this user has liked this stack."""
        return self.likes.filter(user=user).exists()

class Like(CacheMixin, models.Model):
    user = models.ForeignKey(User, related_name="likes")
    stack = models.ForeignKey("Stack", related_name="likes")
    added = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "%s likes %s" % (self.user, self.stack)

    class Meta:
        app_label = 'www'
        unique_together = (("user", "stack"),)

    def invalidate_cache(self):
        # invalidate not individual like instances but collections from each side, user and stack
        incr_version('stack-likes-'+ str(self.stack.id))
        incr_version('user-likes-' + str(self.user.id))
