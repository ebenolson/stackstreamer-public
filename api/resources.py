from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from tastypie.authorization import DjangoAuthorization

from annotations.models import Flag
from stackorg.models import Stack

class StackResource(ModelResource):
    class Meta:
        queryset = Stack.objects.all()
        allowed_methods = ['get']
        filtering = {'uuid':ALL}
        authorization = DjangoAuthorization()

class FlagResource(ModelResource):
    stack = fields.ForeignKey(StackResource, 'stack')
    class Meta:
        queryset = Flag.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = DjangoAuthorization()