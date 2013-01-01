import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.conf import settings
from jinja2 import Environment, PackageLoader
from stacks.www.models import Page

def page(request, topic, slug):
    page = get_object_or_404(Page, topic=topic, slug=slug)
    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))
    template = env.get_template(page.layout.template_file)

    layout_context = {}

    # special items
    layout_context['title'] = page.title
    layout_context['page_stats'] = '... stats ...'

    # grab all of the media items and render
    for page_media_item in page.items.all():
        layout_context[page_media_item.placement] = '<img src="%s%s" />' % (settings.MEDIA_URL, page_media_item.item.image_path)

    # grab all of the text items and render
    for placement, text in page.get_prop('text_items').iteritems():
        layout_context[placement] = markdown.markdown(text)

    # render the layout then render the page
    content = template.render(layout_context)
    return render(request, 'www/page.html', {'page': page, 'content': content})

class PageForm(ModelForm):
    class Meta:
        model = Page

def create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            return HttpResponseRedirect(reverse('page', args=[page.topic, page.slug]))
    else:
        form = PageForm()

    return render(request, 'www/create.html', {'form': form,})

def edit(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name') # this is the ID of the element, which is also the placement name
            value = request.POST.get('value')
            id = request.POST.get('pk')
            page = Page.objects.get(id=id)

            # special case for real schema items
            if name in ('title',):
                setattr(page, name, value)
            # otherwise set properties
            else:
                page.set_path_prop('text_items.' + name, value)

            page.save()
            return HttpResponse()

        except:
            return HttpResponse('There was a problem with saving the attribute.')

