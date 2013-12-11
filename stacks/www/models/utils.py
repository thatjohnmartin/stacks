import re
import unicodedata
from django.db import models
from django.db.utils import IntegrityError

class AutoSlugMixin(models.Model):
    """A mixin to provide auto slug generation."""

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