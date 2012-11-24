from django.shortcuts import render, get_object_or_404
from stacks.www.models import Thing, Post

def home(request):
    latest_things = Thing.objects.order_by('added')[:10]
    latest_posts = Post.objects.order_by('added')[:10]
    return render(request, 'www/home.html', {'latest_things': latest_things, 'latest_posts': latest_posts})

def thing(request, slug):
    thing = get_object_or_404(Thing, slug=slug)
    return render(request, 'www/thing.html', {'thing': thing})