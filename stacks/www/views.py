from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from stacks.www.models import Thing, Post

def home(request):
    latest_things = Thing.objects.order_by('added')[:10]
    latest_posts = Post.objects.order_by('added')[:10]
    return render(request, 'www/home.html', {'latest_things': latest_things, 'latest_posts': latest_posts})

def thing(request, slug):
    thing = get_object_or_404(Thing, slug=slug)
    return render(request, 'www/thing.html', {'thing': thing})

class JoinForm(UserCreationForm):
    email = forms.EmailField()

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/') # !! should redirect to user page
    else:
        form = JoinForm()

    return render(request, 'www/join.html', {'form': form,})
