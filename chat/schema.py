import channels
import channels_graphql_ws
import graphene
from django.utils.timezone import now
from graphene_django.filter import DjangoFilterConnectionField
# from graphql_auth import mutations
# from graphql_auth.schema import MeQuery
# import graphql_jwt
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import OuterRef, Count, Subquery
from django.db.models import Value
from django.db import models
from django.db.models.functions import Coalesce

from graphene_django import DjangoObjectType
from django_filters import FilterSet, CharFilter
from graphene import relay
from graphene.types.generic import GenericScalar

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

import logging
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
from time import strftime

from datetime import datetime
from django.db.models import OuterRef

from chat.models import *
from chat.serializer import * 

User = get_user_model()

class Query(graphene.ObjectType):#MeQuery, 
    me = graphene.Field(ChatUserType)

    users = graphene.List(ChatUserType)
    user_search = graphene.List(ChatUserType, search=graphene.String(), 
                                            first=graphene.Int(), 
                                            skip=graphene.Int(),)

    rooms = DjangoFilterConnectionField(RoomType, filterset_class=RoomFilter)
    room = graphene.Field(RoomType, id=graphene.ID())

    messages = DjangoFilterConnectionField( MessageType, filterset_class=MessageFilter, id=graphene.ID())

    @staticmethod
    def resolve_users(self, info):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in to chat")

        return get_user_model().objects.all()

    @staticmethod
    def resolve_user_search(self, info, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in to chat")

        qs = get_user_model().objects.all()
        
        if search:
            qs = qs.filter(username__icontains=search)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    @staticmethod
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

    @staticmethod
    def resolve_rooms(cls, info, **kwargs): 
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in to chat")

        user = info.context.user 
        return Room.objects.filter(Q(user_id=user) | Q(target=user)).order_by('-last_modified')
            #todo: get last message, is there space in a mobile app? required? later?
            #.annotate(last_message=Message.objects.filter(room_id=OuterRef('pk')[:1])))

    @staticmethod
    def resolve_room(cls, info, id, **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in to chat")

        user = info.context.user
        return Room.objects.get(id=id)

    @staticmethod
    def resolve_messages(cls, info, id, skip=None, last=None,  **kwargs):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in to chat")

        room = Room.objects.get(id=id)
        if user != room.user_id and user != room.target:
            raise Exception('You are not allowed to view this chat')

        #read all except sent by me;
        Message.objects.filter(room_id=room,read__isnull=True).exclude(user_id=user).update(read=datetime.now())
        qs = Message.objects.filter(room_id=room).order_by('-timestamp')
        if skip:
            qs = qs[skip:]

        if last:
            qs = qs[:last]

        return qs

class CreateChat(graphene.Mutation):
    """
    to creeate a chat you need to pass `user_name`
    """
    room = graphene.Field(RoomType)
    error = graphene.String()

    class Arguments:
        user_name = graphene.String(required=True)

    @classmethod
    def mutate(cls, _, info, user_name=None):
        user = info.context.user
        if user is None or not user.is_authenticated:
            raise Exception("You need to be logged in to chat")

        try:
            is_valid_user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            raise Exception("User name not found")

        if info.context.user.username == user_name:
            raise Exception("You can not chat with yourself.")

        room_name_a = [info.context.user.username, user_name]
        room_name_a.sort()
        room_name_str = room_name_a[0]+'_'+room_name_a[1]

        chat_room, _ = Room.objects.get_or_create(name=room_name_str, user_id=User.objects.get(username=room_name_a[0]), target=User.objects.get(username=room_name_a[1]))

        return CreateChat(room=chat_room)

class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        message = graphene.String(required=True)
        room_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, _, info, message, room_id):
        user = info.context.user
        if user is None:
            raise Exception("You need to be logged in to chat")

        room = Room.objects.get(pk=room_id)

        if user != room.user_id and user != room.target:
            raise Exception('You are not allowed to post or view this chat')

        message = Message.objects.create( 
                room_id=room,
                user_id=user,
                content=message,
            )
        
        room.last_modified = datetime.now()
        room.save()

        # if room.user_id == user:
        #     OnNewMessage.broadcast(payload=message, group=room.target.username)
        # else:
        #     OnNewMessage.broadcast(payload=message, group=room.user_id.username)

        OnNewMessage.broadcast(payload=message, group=room.target.username)
        OnNewMessage.broadcast(payload=message, group=room.user_id.username)

        return SendMessage(message=message)


class OnNewMessage(channels_graphql_ws.Subscription):
    message = graphene.Field(MessageType)
    notification_queue_limit = 64

    class Arguments:
        chatroom = graphene.String()

    def subscribe(cls, info, chatroom=None):
        logging.info('subscribe to '+str(chatroom)) 
        return [chatroom] if chatroom is not None else None

    def publish(self, info, chatroom=None):
        return OnNewMessage(
            message=self
        )
        
class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()
    create_chat = CreateChat.Field()

class Subscription(graphene.ObjectType):
    on_new_message = OnNewMessage.Field()
