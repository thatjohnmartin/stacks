from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from stacks.www.models import Page

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']

class PageResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Page.objects.all()
        allowed_methods = ['get']