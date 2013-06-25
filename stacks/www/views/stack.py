from django.shortcuts import render, Http404
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

        layout_context = {}

        # grab all of the media items and render
        # for page_media_item in page.items.all():
        #     layout_context[page_media_item.placement] = '<img src="%s%s" />' % (settings.MEDIA_URL, page_media_item.item.image_path)

        # grab all of the text items and render
        # text_items = stack.get_prop('text_items')
        # if text_items:
        #     for placement, text in text_items.iteritems():
        #         layout_context[placement] = markdown.markdown(text)

        # render the block and add it to the content list
        rendered_blocks.append({'block': block, 'content': template.render(layout_context)})

    return render(request, 'www/stack.html', {'stack': stack, 'rendered_blocks': rendered_blocks})
