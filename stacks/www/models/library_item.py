from django.db import models
from stacks.www.models.utils import PropertiesMixin

class LibraryItem(PropertiesMixin, models.Model):

    # this could include:
    #
    # - uploaded image (jpeg, png, etc)
    # - uploaded FITs file
    # - image URL/ref
    # - video URL/ref
    # - chunk of JSON
    # - chunk of CSV

    class Meta:
        app_label = 'www'