from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.forms import ModelForm
from stacks.www.models import Page

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
