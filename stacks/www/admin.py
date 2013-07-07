from django.contrib import admin
from stacks.www.models import Site, Stack, Block, Layout

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')

admin.site.register(Site, SiteAdmin)

class LayoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'template_file', 'site', 'added')

admin.site.register(Layout, LayoutAdmin)

# class PageMediaItemInline(admin.TabularInline):
#     model = PageMediaItem

class BlockInline(admin.TabularInline):
    fields = ('name', 'layout', 'order', 'properties_json')
    model = Block

class StackAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'site', 'added')
    inlines = [BlockInline,]

admin.site.register(Stack, StackAdmin)
