from django.db import models
from django.contrib.auth import get_user_model
import time

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=128)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="User1") #user 1
    target = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="User2") # user 2
    last_modified = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    deleted = models.PositiveSmallIntegerField(default=0)
    # if None has deleted = 0
    # if user_id has deleted = 1
    # if target has deleted = 2
    # if delete gte 0 = deleet all message of the room;

    def __str__(self):
        return f'{self.name} ({self.user_id}: {self.target}) [{self.last_modified}]'


class Message(models.Model):
    room_id = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE) #user 1
    content = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.DateTimeField(auto_now_add=False,blank=True,null=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f'{self.user_id.username}: {self.content} [{self.timestamp}]'

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.xlsx', '.xls', '.csv', '.txt', '.mp3', '.mp4', '.avi', '.mpg', '.mk4', '.wav', '.zip', '.rar']
    invalid_extensions = ['.exe', '.apk', '.htaccess', '.msi', '.env', '.gitignore']
    if ext.lower() in invalid_extensions:
        raise ValidationError('Unsupported file extension.')

def upload_location(instance, filename):
    filebase, extension = filename.rsplit('.', 2)
    return 'chat_files/%s_%s.%s' % (filebase,time.time(), extension)

class ChatMessageImages(models.Model):
    image = models.FileField(upload_to=upload_location, validators=[validate_file_extension])