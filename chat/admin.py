from django.contrib import admin

# Register your models here.
from chat.models import Room, Message, ChatMessageImages

class CustomRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user_from", "user_to" )
    ordering = ('name',)
    list_filter = ( "name",)
    search_fields = ["name", "user_from__username", "user_from__fullName", "user_from__email", "user_to__username", "user_to__fullName", "user_to__email"]

    def user_from(self, obj):
        return obj.user_id

    def user_to(self, obj):
        return obj.target

class CustomMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room_id", "user_id", "content","read" )
    ordering = ('room_id',)
    list_filter = ( "room_id",)
    search_fields = ('room_id',)

    def room_id(self, obj):
        return Room.objects.get(obj.room_id).name

admin.site.register(Message, CustomMessageAdmin)
admin.site.register(Room, CustomRoomAdmin)
admin.site.register(ChatMessageImages)
