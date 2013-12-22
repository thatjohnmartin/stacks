from djpjax import pjaxtend
from jinja2 import Environment, PackageLoader
from django.shortcuts import Http404
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from stacks.www.models import Stack
from stacks.www.views.stack import render_block

@pjaxtend("www/base_with_navbar.html", "www/pjax.html")
def stacks_home(request):
    return TemplateResponse(request, 'www/stacks_home.html', {})

@pjaxtend("www/base_with_navbar.html", "www/pjax.html")
def site_home(request):
    latest_stacks = Stack.objects.filter(site=request.site).order_by('added')[:20]

    env = Environment(loader=PackageLoader('stacks.www', 'templates/layouts'))

    stack_list = []
    for stack in latest_stacks:
        block = stack.get_featured_block()
        stack_list.append({
            'stack': stack,
            'content': render_block(block, env)
        })

    return TemplateResponse(request, 'www/site_home.html', {'stack_list': stack_list})

@pjaxtend("www/base_with_navbar.html", "www/pjax.html")
def user_home(request, username):
    try:
        page_user = User.objects.get(username=username)
    except:
        raise Http404

    c = {
        'page_user': page_user,
        'is_you': page_user == request.user,
        'stacks': page_user.stacks.all(),
    }

    return TemplateResponse(request, 'www/user_home.html', c)

def tag_home(request):
    return TemplateResponse(request, 'www/tag_home.html')

def tag_list(request, tag):
    return TemplateResponse(request, 'www/tag_list.html')

def test(request):
    return TemplateResponse(request, 'www/test.html')