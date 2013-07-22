from django.http import HttpResponseRedirect

def start(request):
    return HttpResponseRedirect('/astro/')