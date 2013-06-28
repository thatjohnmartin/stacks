import flickrapi
import simplejson
from django.shortcuts import render, Http404
from django.conf import settings
from jinja2 import Environment, PackageLoader
from stacks.www.models import Stack

def stack(request, slug):
    stack = Stack.get_from_cache(site=request.site, slug=slug)
    if not stack:
        raise Http404

    # tell Jinja where to look for templates
    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))

    # build content, rendering each block in order
    rendered_blocks = []
    for block in stack.blocks.order_by('order'):

        template = env.get_template(block.layout.template_file) # !! this should be cached

        layout_context = {'item': item}

        # grab all of the media items and render
        # for page_media_item in page.items.all():
        #     layout_context[page_media_item.placement] = '<img src="%s%s" />' % (settings.MEDIA_URL, page_media_item.item.image_path)

        # grab all of the name/values and render
        pairs = block.get_prop('context')
        if pairs:
            for name, value in pairs.iteritems():
                layout_context[name] = value

        # render the block and add it to the content list
        rendered_blocks.append({'block': block, 'content': template.render(layout_context)})

    return render(request, 'www/stack.html', {'stack': stack, 'rendered_blocks': rendered_blocks})

# this shouldn't live here, just testing!!
def item(type, data):
    if type == 'image':
        if 'type' in data:
            if data['type'] == 'url' and 'url' in data:
                return '<img src="%s" />' % data['url']
            elif data['type'] == 'path' and 'path' in data:
                photo_id = data['path'].split('.').pop()
                flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, format='json')
                sizes = simplejson.loads(flickr.photos_getSizes(photo_id=photo_id)[14:-1])
                for size in sizes['sizes']['size']:
                    if size['label'] == 'Medium 800':
                        return '<img src="%s" />' % size['source']
    return "<i>[Empty]</i>"
