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
    allowedExtension = [".jpg",".png",".ico",".*"]
    sizeLimit = 10240000
    uploader = FileUploader(allowedExtension, sizeLimit)
    return HttpResponse(uploader.handleUpload(request, settings.MEDIA_ROOT + "images/"))

class FileUploader(object):

    def __init__(self, allowedExtensions=None, sizeLimit=None):
        self.allowedExtensions = allowedExtensions or []
        self.sizeLimit = sizeLimit or settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def handleUpload(self, request, uploadDirectory):
        #read file info from stream
        uploaded = request.read
        #get file size
        fileSize = int(uploaded.im_self.META["CONTENT_LENGTH"])
        #get file name
        fileName = uploaded.im_self.META["HTTP_X_FILE_NAME"]
        #check first for allowed file extensions
        #read the file content, if it is not read when the request is multi part then the client get an error
        fileContent = uploaded(fileSize)
        if self._getExtensionFromFileName(fileName) in self.allowedExtensions or ".*" in self.allowedExtensions:
            #check file size
            if fileSize <= self.sizeLimit:
                #upload file
                #write file
                file = open(os.path.join(uploadDirectory, fileName), "wb+")
                file.write(fileContent)
                file.close()
                return simplejson.dumps({"success": True})
            else:
                return simplejson.dumps({"error": "File is too large."})
        else:
            return simplejson.dumps({"error": "File has an invalid extension."})

    def _getExtensionFromFileName(self, fileName):
        filename, extension = os.path.splitext(fileName)
        return extension.lower()
