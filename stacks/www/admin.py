from django.contrib import admin
from stacks.www.models import Page, Layout, MediaItem

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'layout', 'added')

admin.site.register(Page, PageAdmin)
admin.site.register(Layout)
admin.site.register(MediaItem)