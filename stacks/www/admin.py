from django.contrib import admin
from stacks.www.models import Thing, Predicate, Node, Post

class ThingAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'mid', 'added')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('object', 'predicate', 'subject', 'context', 'value_str')

admin.site.register(Thing, ThingAdmin)
admin.site.register(Predicate)
admin.site.register(Node, NodeAdmin)
admin.site.register(Post)
