from django.shortcuts import render, get_object_or_404
from jinja2 import Environment, PackageLoader
from stacks.www.models import Page

def page(request, username, slug):
    page = get_object_or_404(Page, user__username=username, slug=slug)
    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))
    template = env.get_template(page.layout.template_file)
    content = template.render({'foo': 'bar', 'person': 'Isaac Newton'})
    return render(request, 'www/page.html', {'page': page, 'content': content})
