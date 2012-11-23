from django.db import models
from stacks.www.models.utils import PropertiesMixin

class Thing(PropertiesMixin, models.Model):
    name = models.CharField(max_length=255, db_index=True)
    mid = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.CharField(max_length=255, db_index=True, unique=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True) # the date the item was added to the db
    modified = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return self.slug

    class Meta:
        app_label = 'www'

    def get_node(self, predicate_path, context=''):
        p = Predicate.objects.get(path=predicate_path)
        return self.object_nodes.get(predicate=p, context=context)


        '/type/object/key', '/wikipedia/en'

class Predicate(models.Model):
    path = models.CharField(max_length=255, db_index=True, unique=True)

    def __unicode__(self):
        return self.path

    class Meta:
        app_label = 'www'

class Node(PropertiesMixin, models.Model):
    object = models.ForeignKey('Thing', related_name="object_nodes")
    predicate = models.ForeignKey('Predicate')
    subject = models.ForeignKey('Thing', null=True, related_name="subject_nodes")
    context = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    value_int = models.IntegerField(null=True, blank=True, db_index=True)
    value_str = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    value_date = models.DateTimeField(null=True, blank=True, db_index=True)

    def __unicode__(self):
        value = ""
        if self.subject:
            value = self.subject
        else:
            if self.value_int:
                value = self.value_int
            if self.value_str:
                value = self.value_str
            if self.value_date:
                value = self.value_date
        return '(%s) %s (%s)' % (self.object, self.predicate, value)

    class Meta:
        app_label = 'www'
