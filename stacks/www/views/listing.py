from django.shortcuts import render, Http404
from django.contrib.auth.models import User
from stacks.www.models import Stack

def stacks_home(request):
    latest_stacks = Stack.objects.filter().order_by('added')[:20]
    return render(request, 'www/stacks_home.html', {'latest_stacks': latest_stacks})

def site_home(request):
    latest_stacks = Stack.objects.filter(site=request.site).order_by('added')[:20]
    return render(request, 'www/site_home.html', {'latest_stacks': latest_stacks})

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

    return render(request, 'www/user_home.html', c)

def tag_home(request):
    return render(request, 'www/tag_home.html')

def tag_list(request, tag):
    return render(request, 'www/tag_list.html')

def test(request):
    return render(request, 'www/test.html')