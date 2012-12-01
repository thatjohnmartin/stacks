import os
from django.views.generic import CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def upload(request):
    allowed_extensions = [".jpg", ".png", ".ico", ".*"]
    size_limit = 1024 * 1000 * 10 # 10mb
    uploader = FileUploader(allowed_extensions, size_limit)
    result = uploader.handle_upload(request, settings.MEDIA_ROOT + "images/")
    if result == 'bad':
        return 'bad'
    else:
        # create media item
        pass
    return HttpResponse()

class FileUploader(object):

    def __init__(self, allowed_extensions=None, size_limit=None):
        self.allowed_extensions = allowed_extensions or []
        self.size_limit = size_limit or settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def handle_upload(self, request, upload_directory):
        # read file info from stream
        uploaded = request.read
        # get file size
        file_size = int(uploaded.im_self.META["CONTENT_LENGTH"])
        # get file name
        file_name = uploaded.im_self.META["HTTP_X_FILE_NAME"]
        # check first for allowed file extensions
        # read the file content, if it is not read when the request is multi part then the client get an error
        file_content = uploaded(file_size)
        if self._get_extension(file_name) in self.allowed_extensions or ".*" in self.allowed_extensions:
            # check file size
            if file_size <= self.size_limit:
                # upload file
                # write file
                file = open(os.path.join(upload_directory, file_name), "wb+")
                file.write(file_content)
                file.close()
                return simplejson.dumps({"success": True})
            else:
                return simplejson.dumps({"error": "File is too large."})
        else:
            return simplejson.dumps({"error": "File has an invalid extension."})

    def _get_extension(self, file_name):
        name, extension = os.path.splitext(file_name)
        return extension.lower()
