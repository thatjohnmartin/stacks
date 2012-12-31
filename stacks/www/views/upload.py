import os
import datetime
from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from stacks.www.models import MediaItem

ALLOWED_EXTENSIONS = [".jpg", ".png", ".gif"]
SIZE_LIMIT = 1024 * 1000 * 10 # 10mb

def _get_extension(name):
    name_without_extension, extension = os.path.splitext(name)
    return extension.lower()

@csrf_exempt
def upload_image(request):
    uploaded = request.read
    name = uploaded.im_self.META["HTTP_X_FILE_NAME"]

    # create a directory path with today's date and make sure it exists
    directory_path_from_media_root = os.path.join("images", datetime.datetime.now().strftime('%Y/%m/%d'))
    full_directory_path = os.path.join(settings.MEDIA_ROOT, directory_path_from_media_root)
    if not os.path.exists(full_directory_path):
        os.makedirs(full_directory_path)

    file_path_from_media_root = os.path.join(directory_path_from_media_root, name)
    size = int(uploaded.im_self.META["CONTENT_LENGTH"])
    file_content = uploaded(size)
    if _get_extension(name) in ALLOWED_EXTENSIONS or ".*" in ALLOWED_EXTENSIONS:
        if size <= SIZE_LIMIT:
            file = open(os.path.join(settings.MEDIA_ROOT , file_path_from_media_root), "wb+")
            file.write(file_content)
            file.close()
        else:
            return HttpResponse(simplejson.dumps({'error': "File is too large."}))
    else:
        return HttpResponse(simplejson.dumps({'error': "File has an invalid extension."}))

    item = MediaItem.objects.create(
        user = request.user,
        title = name,
        image_path = file_path_from_media_root,
    )
    return HttpResponse(simplejson.dumps({'success': True, 'path': settings.MEDIA_URL + file_path_from_media_root}))
