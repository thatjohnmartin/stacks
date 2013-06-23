from django.shortcuts import render
from stacks.www.models import Page

def home(request):
    latest_pages = Page.objects.filter(site=request.site).order_by('added')[:20]
    return render(request, 'www/home.html', {'latest_pages': latest_pages})

def user_home(request, username):
    return render(request, 'www/user_home.html')

def tag_home(request):
    return render(request, 'www/tag_home.html')

def tag_list(request, tag):
    return render(request, 'www/tag_list.html')

def test(request):
    return render(request, 'www/test.html')