from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm
from stacks.www.models import Thing, Post

def home(request):
    latest_things = Thing.objects.order_by('added')[:10]
    latest_posts = Post.objects.order_by('added')[:10]
    return render(request, 'www/home.html', {'latest_things': latest_things, 'latest_posts': latest_posts})

def thing(request, slug):
    thing = get_object_or_404(Thing, slug=slug)
    return render(request, 'www/thing.html', {'thing': thing,})

class JoinForm(UserCreationForm):
    email = forms.EmailField()
    # !! fix error messages. need one for email and to make them display properly on the page
    # !! also, add a stopword list for URLs that the system needs, e.g. signin, signout, upload, organize, etc

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/') # !! should redirect to user page
    else:
        form = JoinForm()

    return render(request, 'www/join.html', {'form': form,})

def upload(request):
    return render(request, 'www/upload.html')

def create(request):
    return render(request, 'www/create.html')

def user_home(request, username):
    return render(request, 'www/user_home.html')

def topic_home(request, topic):
    return render(request, 'www/topic_home.html', {'topic': topic})