import logging
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger('utils.cache')

#
# New cache utilities for the web app - intended for use by the CacheMixin and more.
#

# usage example:
#
#    getting a single thing from the account namespace:
#
#        my_segment = get_from_cache(
#            version_key('segment-' + my_segment.code, account),
#            lambda: account.segments.all().order_by('name'))
#
#    getting a list of things from the account namespace:
#
#        all_segments = get_from_cache(
#            version_key('segments', account) + '.all',
#            lambda: account.segments.all().order_by('name'))
#
#    getting a single thing from the global namespace:
#
#        account = get_from_cache(
#            version_key('account-' + account_code),
#            lambda: Account.objects.get(code=account_code))
#
#    invalidating things in the account namespace:
#
#        def invalidate_cache(self):
#            incr_version('segments', self.account)
#            incr_version('segment-' + self.id, self.account)

def _version_number_key(key):
    return key + '.version'

def get_version(key):
    "Get a version number from the cache, or create one if it doesn't exist."
    version_key = _version_number_key(key)
    version = cache.get(version_key)
    if not version:
        if settings.ENABLE_CACHE_LOGGING:
            log.debug('CACHE: Creating new version key %s' % version_key)
        cache.set(version_key, 1)
        version = 1
    return version

def version_key(name, prefix=None):
    "Generate a key with the latest version number from the cache, use an Account or User or string as a prefix."
    key = _gen_key_with_prefix(name, prefix)
    return '%s:%s' % (key, get_version(key))

def get_from_cache(key, f, ttl=60*60*23):
    "Get an item from the cache, or update it if it's not there, default to 48 hour TTL."
    item = cache.get(key)
    if item is None: # specifically checking against None, so 0, [], etc get through
        item = f()
        cache.set(key, item, ttl)
        if settings.ENABLE_CACHE_LOGGING:
            log.debug('CACHE: Adding item to cache at %s' % (key, ))
    else:
        if settings.ENABLE_CACHE_LOGGING:
            log.debug('CACHE: Found cached item at %s' % key)
    return item

def incr_version(name, prefix=None):
    "Increment the version of an item, or create one if it doesn't exist."
    key = _gen_key_with_prefix(name, prefix) + '.version'
    try:
        cache.incr(key)
        if settings.ENABLE_CACHE_LOGGING:
            log.debug('CACHE: Increment version key %s' % key)
    except ValueError:
        cache.add(key, 1)
        if settings.ENABLE_CACHE_LOGGING:
            log.debug('CACHE: Create version key %s' % key)

def _gen_key_with_prefix(name, prefix=None):
    prefix_string = ''
    if prefix:
        # cheat and avoid circular (and unnecessary) imports by grabbing a str version of the class name
        cls = prefix.__class__.__name__
        if cls == 'User':
            prefix_string = 'user-' + str(prefix.id) + '-'
        else:
            prefix_string = str(prefix) + '-'
    return prefix_string + name