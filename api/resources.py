from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization

from annotations.models import Flag
from stackorg.models import Stack

class StackResource(ModelResource):
    class Meta:
        queryset = Stack.objects.all()
        allowed_methods = ['get']
        authorization = DjangoAuthorization()

class FlagResource(ModelResource):
    stack = fields.ForeignKey(StackResource, 'stack')
    class Meta:
        queryset = Flag.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = DjangoAuthorization()