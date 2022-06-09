import graphene
from django.contrib.auth import get_user_model
from django_filters import FilterSet, OrderingFilter
from graphene import relay
from graphene_django import DjangoObjectType
from django.db.models import Q

from chat.models import *

# class UserFilter(FilterSet):
#     class Meta:
#         model = get_user_model()
#         fields = ('username', "email", "last_name", "first_name", "id",)
#         order_by = ("id",)

class ChatUserType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', "email", "last_name", "first_name", "id"]
        interfaces = (relay.Node,)


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = ("last_modified", "name", "user_id", "target")
        order_by = ("last_modified", "id",)

class RoomType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Room
        fields = '__all__'
        interfaces = (relay.Node,)


class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = ("room_id","user_id", "content", "read", 'timestamp',)
        order_by = ('-timestamp', "id")

class MessageType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Message
        fields = '__all__'
        interfaces = (relay.Node,)