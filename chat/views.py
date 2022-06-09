from django import forms  
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.forms import fields  
from django.urls import reverse
import os
from time import gmtime, strftime

from chat.models import Room, Message, ChatMessageImages, User

class ChatImagesFrm(forms.ModelForm):
    class Meta:  
        # To specify the model to be used to create form  
        model = ChatMessageImages
        # It includes all the fields of model  
        fields = '__all__'  

def image_upload(request):
    if not request.user.is_authenticated:
        return JsonResponse({"err":"not logged in"}, safe=False)

    if request.method == 'POST':
        form = ChatImagesFrm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
  
            # Getting the current instance object to display in the template  
            img_object = form.instance

            return JsonResponse({"img":str(img_object.image.url),"ret":True}, safe=False)
        else:
            return JsonResponse({"err":form.errors}, safe=False)

    return JsonResponse({"err":"no post"}, safe=False)

