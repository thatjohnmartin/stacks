from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm

class JoinForm(UserCreationForm):
    email = forms.EmailField()
    # !! fix error messages. need one for email and to make them display properly on the page
    # !! also, add a stopword list for URLs that the system needs, e.g. signin, signout, upload, organize, etc

def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse("login")) # !! should redirect to user page
    else:
        form = JoinForm()

    return render(request, 'www/join.html', {'form': form,})
