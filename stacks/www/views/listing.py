from django.shortcuts import render
from stacks.www.models import Page

def home(request):
    latest_pages = Page.objects.order_by('added')[:20]
    return render(request, 'www/home.html', {'latest_pages': latest_pages})

def topic_home(request, topic):
    pages = Page.objects.filter(topic=topic).order_by('added')[:20]
    return render(request, 'www/topic_home.html', {'topic': topic,'latest_pages': pages})

def user_home(request, username):
    return render(request, 'www/user_home.html')
