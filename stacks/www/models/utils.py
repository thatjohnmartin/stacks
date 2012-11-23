import re
import unicodedata
import simplejson

from django.db import models
from django.db.utils import IntegrityError

class PropertiesMixin(models.Model):
    """model-class mixin adds generic p-list via carrier 'properties_json' field containing JSON-encoded property dict"""
    # note this is an abstract Django 1.0+ model class, inheritors don't need to add the properties_json field

    properties_json = models.TextField(null=True, blank=True) # carries the p-list dict as JSON-encoded text

    class Meta:
        abstract = True

    @property
    def properties(self):
        if not hasattr(self, '_properties'):
            if not self.properties_json:
                self._properties = {}
            else:
                try:
                    self._properties = simplejson.loads(self.properties_json)
                except ValueError, ex:
                    self._properties = {}
            self._props_dirty = False
        return self._properties

    def get_prop(self, prop_name, default=None):
        "retrieves named property"
        return self.properties.get(prop_name, default)

    def get_path_prop(self, prop_pathname, default=None):
        "utility getter for traversing a nested dict with a dotted pathname"
        prop = self.properties
        for n in prop_pathname.split('.'):
            if not prop or n not in prop: return default
            prop = prop[n]
        return prop

    def set_prop(self, prop_name, value):
        "sets named property value"
        self.properties[prop_name] = value
        self._props_dirty = True
        return value

    def set_path_prop(self, pathname, value):
        "set property in nested dictionaries from dotted pathname"
        prop = self.properties
        paths = pathname.split('.')
        for n in paths[:-1]:
            if n not in prop:
                prop[n] = {}
            prop = prop[n]
        prop[paths[-1]] = value
        self._props_dirty = True
        return value

    def update_props(self, new_props, recursive=False):
        "updates props from given new_props dict"
        if recursive:
            def update_props_recursive(current, new):
                for k, v in new.items():
                    if isinstance(v, dict) and isinstance(current.get(k), dict):
                        # recurse down matching nested dicts
                        update_props_recursive(current[k], v)
                    else:
                        # updates leafs from new_props
                        current[k] = v
            update_props_recursive(self.properties, new_props)
        else:
            self.properties.update(new_props)
        self._props_dirty = True

    def del_prop(self, prop_name):
        "delete a property"
        if prop_name in self.properties:
            del self.properties[prop_name]
            self._props_dirty = True

    def del_path_prop(self, pathname):
        "delete leaf in nested dictionaries from dotted pathname"
        prop = self.properties
        paths = pathname.split('.')
        for n in paths[:-1]:
            if n not in prop:
                prop[n] = {}
            prop = prop[n]
        if paths[-1] in prop:
            del prop[paths[-1]]
            self._props_dirty = True

    def props_changed(self):
        "signal prop change under the hood, mark dirty for save"
        self._props_dirty = True

    def save(self, **kwargs):
        if getattr(self, '_props_dirty', False):
            self.properties_json = simplejson.dumps(self._properties)
        super(PropertiesMixin, self).save(**kwargs)

class CacheMixin(models.Model):
    "A mixin that provides scaffolding for cache invalidation."

    class Meta:
        abstract = True

    def save(self, **kwargs):
        super(CacheMixin, self).save(**kwargs)
        self.invalidate_cache()

    def delete(self, **kwargs):
        super(CacheMixin, self).delete(**kwargs)
        self.invalidate_cache()
        # Note: I don't think the delete will capture query_set deletions, so at some point we
        # should add some signal-based invalidation.

    def invalidate_cache(self):
        pass

class AutoSlugMixin(models.Model):
    "A mixin to provide auto slug generation."

    slug = models.CharField(max_length=100, null=False, blank=True, db_index=True, unique=True)

    class Meta:
        abstract = True

    def _slugify(value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        return re.sub('[-\s]+', '-', value)

    def save(self, **kwargs):
        if self.slug:
            super(AutoSlugMixin, self).save(**kwargs)
        else:
            saved = False
            i = 0
            while not saved:
                self.slug = self._slugify(self.title)
                if i:
                    self.slug += '-' + i

                try:
                    super(AutoSlugMixin, self).save(**kwargs)
                    saved = True
                except IntegrityError, ex:
                    # if the error is a duplicate slug, then retry, else throw
                    if ex.args[0] == 1062 and ex.args[1].find(self.slug) != -1:
                        i += 1
                        continue
                    else:
                        raise ex