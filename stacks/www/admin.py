from django.contrib import admin
from stacks.www.models import Page, PageMediaItem, Layout, MediaItem

class LayoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'template_file', 'added')

admin.site.register(Layout, LayoutAdmin)

class PageMediaItemInline(admin.TabularInline):
    model = PageMediaItem

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'layout', 'added')
    inlines = [PageMediaItemInline,]

admin.site.register(Page, PageAdmin)

class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_path', 'user', 'added')

admin.site.register(MediaItem, MediaItemAdmin)