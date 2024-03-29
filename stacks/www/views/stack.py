import flickrapi
import simplejson
import markdown
import StringIO
import csv
import urllib2
from jinja2 import Environment, PackageLoader
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms import ModelForm
from stacks import directory
from stacks.www.models import Stack, Block
from stacks import constants
from decentscraper import scrape

def stack(request, slug):
    stack = Stack.get_from_cache(site_id=request.site.id, slug=slug)
    if not stack:
        raise Http404

    # tell Jinja where to look for templates
    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))

    # build content, rendering each block in order
    rendered_blocks = []
    for block in stack.blocks.order_by('order'):
        rendered_blocks.append({'block': block, 'content': render_block(block, env)})

    c = {
        'stack': stack,
        'is_you': stack.user == request.user,
        'rendered_blocks': rendered_blocks
    }

    return render(request, 'www/stack.html', c)

def block(request, slug, block_id):
    block = Block.objects.get(id=block_id)
    if not block:
        raise Http404

    # tell Jinja where to look for templates
    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))

    content = render_block(block, env)

    c = {
        'block': block,
        'content': content,
        'is_you': block.stack.user == request.user,
    }

    return render(request, 'www/block.html', c)

def render_block(block, template_env, render_as_feature=False):
    template = template_env.get_template(block.layout.template_file) # !! this should be cached

    layout_context = {'item': item, 'render_as_feature': render_as_feature}

    pairs = block.properties_json['context']
    if pairs:
        for name, value in pairs.iteritems():
            layout_context[name] = value

    return template.render(layout_context)

class StackForm(ModelForm):
    class Meta:
        model = Stack

def new(request):
    if request.method == 'POST':
        form = StackForm(request.POST)
        if form.is_valid():
            page = form.save()
            return HttpResponseRedirect(reverse('stack', args=[stack.site, stack.slug]))
    else:
        form = StackForm()

    return render(request, 'www/create.html', {'form': form,})

def parse_type(type):
    """Parses a (mime)type string into super-type and sub-type."""
    if type not in constants.SUPPORTED_TYPES:
        raise Exception('Unsupported type: %s.' % type)
    # guaranteed to have 2 bits after a split now
    return type.split('/') # i.e. returns (super_type, sub_type)

def parse_type_list(type_list):
    """Parses a list of types and returns a list of (super-type, sub-type) tuples."""
    parsed_types = []
    for type in type_list:
        parsed_types.append((parse_type(type)))
    return parsed_types

def type_matches(super_type1, sub_type1, super_type2, sub_type2):
    """Returns true if the type2 exactly matches type1, or matches super-type where type1 has a wildcard sub-type."""
    if super_type1 == super_type2:
        if sub_type1 == '*' or sub_type1 == sub_type2:
            return True
    return False

def type_in_list(super_type, sub_type, type_list):
    """Returns true if the given type is matched by a type in the list."""
    for super_type1, sub_type1 in type_list:
        if type_matches(super_type1, sub_type1, super_type, sub_type):
            return True
    return False

def item(placement_types, data, render_as_feature=False):
    """Renders a typed template item."""

    def _render_item_error(message):
        return '<div class="alert">%s</div>' % message

    def _render_missing_param_error(param_name):
        return _render_item_error("Missing parameter <i>%s</i> for <i>%s</i> item." % (param_name, placement_types))

    # pull out the super/sub types that the placement asks for and check that they are supported
    try:
        types = parse_type_list(placement_types)
    except:
        return _render_item_error("Unsupported type: %s" % placement_types)

    # check that the type of the data matches up
    data_super_type, data_sub_type = parse_type(data['type'])
    if not type_in_list(data_super_type, data_sub_type, types):
        _render_item_error("Item type not supported in placement. Found %s but need %s." % (data['type'], placement_types))

    # check for a provider and default to inline
    provider = data['provider'] if 'provider' in data else 'inline'

    # image rendering - supports all formats and url and flickr providers
    if data_super_type == 'image':

        # ignore the sub_type for images ... it doesn't matter

        # get the image item template
        env = Environment(loader=PackageLoader('stacks.www', 'templates/items'))
        template = env.get_template('image.html') # !! this should be cached
        c = {}
        c['render_as_feature'] = render_as_feature

        if provider == 'url':
            if 'url' not in data:
                return _render_missing_param_error('url')
            c['image_url'] = data['url']

        elif provider == 'flickr':
            if 'photo_id' not in data:
                return _render_missing_param_error('photo_id')

            photo_id = data['photo_id']
            flickr = flickrapi.FlickrAPI(settings.FLICKR_API_KEY, format='json')
            sizes = simplejson.loads(flickr.photos_getSizes(photo_id=photo_id)[14:-1])
            for size in sizes['sizes']['size']:
                if size['label'] == 'Medium 800':
                    c['image_url'] = size['source']

            info = simplejson.loads(flickr.photos_getInfo(photo_id=photo_id)[14:-1])
            url = info['photo']['urls']['url']
            if url and url[0]['type'] == 'photopage':
                    c['page_url'] = url[0]['_content']

        if 'image_url' in c:
            return template.render(c)

    # text rendering - supports plain, html, markdown formats and inline
    if data_super_type == 'text' and data_sub_type != 'csv':

        if provider == 'inline':
            if 'value' not in data:
                return _render_missing_param_error('value')

            # use the markdown processor for both plain text and actual markdown
            if data_sub_type in ('plain', 'x-markdown'):
                return markdown.markdown(data['value'])

            elif data_sub_type == 'html':
                return data['value']

    # table rendering - supports csv format and inline provider
    if data_super_type == 'text' and data_sub_type == 'csv':

        # get the table item template
        env = Environment(loader=PackageLoader('stacks.www', 'templates/items'))
        template = env.get_template('table.html') # !! this should be cached
        c = {}

        f = None

        if provider == 'inline':
            if 'value' not in data:
                _render_missing_param_error('value')

            f = StringIO.StringIO(data['value'])

        elif provider == 'url':
            if 'url' not in data:
                _render_missing_param_error('url')

            f = urllib2.urlopen(data['url'])

        if f:
            # delimiter is configurable
            delimiter = data['delimiter'] if 'delimiter' in data else ','

            reader = csv.reader(f, delimiter=delimiter)

            # if there is a header row, pop it off the reader
            if 'use_row_header' in data and data['use_row_header'] == True:
                c['header_row'] = reader.next()
                c['use_row_header'] = True
            else:
                c['use_row_header'] = False

            # pull the rest of the rows
            c['rows'] = [row for row in reader]

            # other options
            c['use_col_header'] = data['use_col_header'] if 'use_col_header' in data else False
            c['style'] = data['style'] if 'style' in data else []

            return template.render(c)

    if data_super_type == 'application' and data_sub_type == 'x-route-topo-json':

        # get the image item template
        env = Environment(loader=PackageLoader('stacks.www', 'templates/items'))
        template = env.get_template('climbing/topo.html') # !! this should be cached
        c = {}

        c['topo'] = scrape(provider, data_sub_type, data['value']['_scrape']['url'])

        return template.render(c)

    if data_super_type == 'application' and data_sub_type == 'x-astro-object-json':

        # get the image item template
        env = Environment(loader=PackageLoader('stacks.www', 'templates/items'))
        template = env.get_template('astro/object_attributes.html') # !! this should be cached
        c = {}

        c['astro_object_attributes'] = scrape(provider, data_sub_type, data['value']['_scrape']['url'])

        return template.render(c)

    if data_super_type == 'application' and data_sub_type == 'x-stacks-directory':

        # get the image item template
        env = Environment(loader=PackageLoader('stacks.www', 'templates/items'))
        template = env.get_template('astro/object_attributes.html') # !! this should be cached
        c = {}

        # c['astro_object_attributes'] = scrape(provider, data_sub_type, data['value']['_scrape']['url'])
        c['astro_object_attributes'] = directory[data['path']]

        return template.render(c)

    # simple error message for unprocessed items
    return _render_item_error("Empty")
