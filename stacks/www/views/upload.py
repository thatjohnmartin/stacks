import os
from django.views.generic import CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.conf import settings
from stacks.www.models import MediaItem

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
        url = settings.MEDIA_URL + str(self.object.image_file)
        data = [{
            'name': f.name,
            'url': url,
            'thumbnail_url': url,
            'delete_url': reverse('upload_delete', args=[self.object.id]),
            'delete_type': "DELETE"
        }]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

class MediaItemDeleteView(DeleteView):
    model = MediaItem

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect(reverse('upload_new'))

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse,self).__init__(content, mimetype, *args, **kwargs)
