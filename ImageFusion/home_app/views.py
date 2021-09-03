from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from . models import UploadedImages
from django.contrib import messages
import os
# Create your views here.
def home(request):
    return render(request, 'index.html')

def upload_images(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        username = request.user
        email = request.user.email
        if request.method == 'GET':
            if username is not None and email is not None:
                all_images = UploadedImages.objects.filter(email=email, username=username)
                if all_images is not None:
                    return render(request, 'home_app/uploadImage.html', {'all_images': all_images})
                else:
                    return render(request, 'home_app/uploadImage.html')
            else:
                return render(request, 'home_app/uploadImage.html')
        else:
            images = request.FILES.getlist('images')
            for img in images:
                UploadedImages.objects.create(username=username, email=email, images=img)
            all_images = UploadedImages.objects.filter(email=email, username=username)
            return render(request, 'home_app/uploadImage.html', {'all_images': all_images})

def login(request):
    return render(request, 'login.html')

def delete_image(request, pk):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        obj = UploadedImages.objects.get(id=pk)
        if len(obj.images) > 0:
            os.remove(obj.images.path)
        obj.delete()
        messages.success(request, 'Image Deleted Successfully !')
        return redirect('/upload_images/')
    
def delete_all_images(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        obj = UploadedImages.objects.filter(username=request.user, email=request.user.email)
        for i in obj:
            if len(i.images) > 0:
                os.remove(i.images.path)
        obj.delete()
        messages.success(request, 'All Images Deleted Successfully !')
        return redirect('/upload_images')

def image_processing(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        username = request.user
        email = request.user.email
        if request.method == 'GET':
            if username is not None and email is not None:
                all_images = UploadedImages.objects.filter(email=email, username=username)
                if all_images is not None:
                    return render(request, 'home_app/image_processing.html', {'all_images': all_images})
                else:
                    return render(request, 'home_app/image_processing.html')
            else:
                return render(request, 'home_app/image_processing.html')
        else:
            pass

def image_fusion(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        image_objects_list = []
        checked_images_id = request.POST.getlist('image_checkbox')
        print('ID of checked images : ' + str(checked_images_id)) #
        if checked_images_id:
            print('Some Images or All Images') #
            for i in checked_images_id:
                image_object = UploadedImages.objects.get(id=i)
                image_objects_list.append(image_object.images)
            print(image_objects_list) #
            return redirect('/image_processing')
        else:
            print('Empty') #
            return redirect('/image_processing')