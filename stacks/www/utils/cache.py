import logging
import re
import hashlib
from django.core.cache import cache
from django.conf import settings
from django.utils.encoding import smart_str

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

def safe_cache_key(key, no_limit=False):
    ''' Returns a safe cache key
    (esp. for memcache which has restrictions on what keys are valid).

    Replaces invalid memcache control characters with an underscore.
    If len is > 240 will return part of the value plus an md5 hexdigest of value.

    (set to 240 and not 250 because Django can prepend prefix and version numbers)
    '''
    # force to bytestring to make any unicode safe for memcached
    cache_key = smart_str(key, encoding='ascii', errors='ignore')
    if len(cache_key) > 240:
        if no_limit == False:
            # use a subset of data to form the cache key
            cache_key = cache_key[:200] + '-' + hashlib.md5(cache_key[:500]).hexdigest()
        else:
            cache_key = hashlib.md5(cache_key).hexdigest()

    # remove any characters not between ascii 33 and 127 for memcached
    cache_key = re.sub(ur'[^\u0021-\u007F]', '-', cache_key, re.UNICODE)
    return cache_key

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