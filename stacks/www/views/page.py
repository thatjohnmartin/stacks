from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from jinja2 import Environment, PackageLoader
from stacks.www.models import Page

def page(request, topic, slug):
    page = get_object_or_404(Page, topic=topic, slug=slug)
    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))
    template = env.get_template(page.layout.template_file)
    content = template.render({'foo': 'bar', 'person': 'Isaac Newton'})
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
            name = request.POST.get('name')
            value = request.POST.get('value')
            id = request.POST.get('pk')
            page = Page.objects.get(id=id)
            setattr(page, name, value)
            page.save()
            return HttpResponse()
        except:
            return HttpResponse('There was a problem with saving the attribute.')

