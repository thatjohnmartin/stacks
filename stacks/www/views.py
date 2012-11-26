from django.views.generic import CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from stacks.www.models import MediaItem

def home(request):
    return render(request, 'www/home.html', {})

#def thing(request, slug):
#    thing = get_object_or_404(Thing, slug=slug)
#    return render(request, 'www/thing.html', {'thing': thing,})

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

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class MediaItemCreateView(CreateView):
    model = MediaItem

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('image_file')
        data = [{
            'name': f.name,
            'url': settings.MEDIA_URL + "images/" + f.name.replace(" ", "_"),
            'thumbnail_url': settings.MEDIA_URL + "images/" + f.name.replace(" ", "_"),
            'delete_url': reverse('upload-delete', args=[self.object.id]),
            'delete_type': "DELETE"
        }]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class MediaItemDeleteView(DeleteView):
    model = MediaItem

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/upload/new')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse,self).__init__(content, mimetype, *args, **kwargs)
