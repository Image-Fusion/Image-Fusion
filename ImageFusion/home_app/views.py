from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from . models import UploadedImages, ImageFusionUploadedImages
from django.contrib import messages
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from PIL import Image
import numpy as np
from django.core.files.storage import default_storage
import base64
import pywt
import cv2

# Create your views here.

def home(request):
    return render(request, 'index.html')

@login_required
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

@login_required
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
    
@login_required
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

@login_required
def image_processing(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        username = request.user
        email = request.user.email
        if request.method == 'GET':
            if username is not None and email is not None:
                all_images = UploadedImages.objects.filter(email=email, username=username)
                # numbers_list = []
                # for i in range(0, len(all_images)):
                #     numbers_list.append(i)
                # html_list = []
                # for row in all_images:
                #     path = row.images.url
                #     path_list = path.split("/")[-1:]
                #     string_path = 'F:/Adit/TE3/TE-Projects/Django/Image-Fusion/ImageFusion/static/images/' + str(path_list[0])
                #     data = open(string_path, 'rb').read()
                #     bytes_base64 = base64.b64encode(data)
                #     text_base64 = bytes_base64.decode()
                #     print(text_base64)
                #     print("\n\n\n")
                #     html = '<img class="card-img-top" src="data:image/tiff;base64,' + text_base64 + '">'
                #     html_list.append(html)
                #     # open('output-tiff.html', 'w').write(html)
                if all_images is not None:
                    return render(request, 'home_app/image_processing.html', {'all_images': all_images})
                else:
                    return render(request, 'home_app/image_processing.html')
            else:
                return render(request, 'home_app/image_processing.html')
        else:
            pass

def avg_min_max(request, image_objects_list):
    # Open Image Files
    with Image.open('static/images/' + str(image_objects_list[0])) as img_1:
        with Image.open('static/images/' + str(image_objects_list[1])) as img_2:
            # Load 
            px_1 = img_1.load()
            px_2 = img_2.load()
            # Image Size {Single Value for Single Band Image(eg. Grayscale Image) and Tuple for Multi Band Image(eg. RGB Image)}
            image_size_1 = img_1.size
            image_size_2 = img_2.size
            width_1, height_1 = img_1.size
            new_size = (width_1, height_1)
            img_avg = Image.new(mode="L", size=new_size)
            img_min = Image.new(mode="L", size=new_size)
            img_max = Image.new(mode="L", size=new_size)
            image_size_avg = img_avg.size
            image_size_min = img_min.size
            image_size_max = img_max.size
            # Print Image Size in (width, height)
            print("Image_size_1 : " + str(image_size_1))
            print("Image_size_2 : " + str(image_size_1))
            print("Image_size_avg : " + str(image_size_avg))
            print("Image_size_min : " + str(image_size_min))
            print("Image_size_max : " + str(image_size_max))
            # If Image Size is Equal
            if image_size_1 == image_size_2:
                # Getting Pixel Location as (x, y)
                for i in range(0, image_size_1[0]):
                    for j in range(0, image_size_1[1]):
                        x, y = i, j
                        # Getting Pixel COLOR at location (x, y) from First Image
                        pixel_color_image_1 = img_1.getpixel((x, y))
                        # Getting Pixel COLOR at location (x, y) from Second Image
                        pixel_color_image_2 = img_2.getpixel((x, y))
                        # Calculating Average from both Pixel's COLOR
                        color_output_avg = (pixel_color_image_1 + pixel_color_image_2) // 2
                        # Calculating Minimum Pixel COLOR from both Pixel's COLOR
                        color_min = int(np.min([pixel_color_image_1, pixel_color_image_2]))
                        # Calculating Maximum Pixel COLOR from both Pixel's COLOR
                        color_max = int(np.max([pixel_color_image_1, pixel_color_image_2]))
                        # Replacing Pixel's OLD COLOR value with NEW COLOR value
                        img_avg.putpixel((x, y), color_output_avg)
                        img_min.putpixel((x, y), color_min)
                        img_max.putpixel((x, y), color_max)
                print("Task completed")
            username = request.user
            email = request.user.email
            path_avg = 'static/images/'+'avg'+'.png'
            path_min = 'static/images/'+'min'+'.png'
            path_max = 'static/images/'+'max'+'.png'
            img_avg.save(path_avg) 
            img_min.save(path_min) 
            img_max.save(path_max)  
            for i in [path_avg, path_min, path_max]:
                print(i)
                print("::::::::::::::::::::::::::::")
                ImageFusionUploadedImages.objects.create(username=username, email=email, images=i)
# This function does the coefficient fusing according to the fusion method
def fuseCoeff(cooef1, cooef2, method):
    if (method == 'mean'):
        cooef = (cooef1 + cooef2) / 2
    elif (method == 'min'):
        cooef = np.minimum(cooef1,cooef2)
    elif (method == 'max'):
        cooef = np.maximum(cooef1,cooef2)
    else:
        cooef = []
    return cooef

def wavelet(request, image_objects_list):
    # Params
    FUSION_METHOD = 'mean' # Can be 'min' || 'max || anything you choose according theory
    # Read the two image
    I1 = cv2.imread('static/images/' + str(image_objects_list[0]),0)
    I2 = cv2.imread('static/images/' + str(image_objects_list[1]),0)
    # We need to have both images the same size
    I2 = cv2.resize(I2,I1.shape) # I do this just because i used two random images
    ## Fusion algo
    # First: Do wavelet transform on each image
    wavelet = 'db1'
    cooef1 = pywt.wavedec2(I1[:,:], wavelet)
    cooef2 = pywt.wavedec2(I2[:,:], wavelet)
    # Second: for each level in both image do the fusion according to the desire option
    fusedCooef = []
    for i in range(len(cooef1)-1):
        # The first values in each decomposition is the apprximation values of the top level
        if(i == 0):
            fusedCooef.append(fuseCoeff(cooef1[0],cooef2[0],FUSION_METHOD))
        else:
            # For the rest of the levels we have tupels with 3 coeeficents
            c1 = fuseCoeff(cooef1[i][0],cooef2[i][0],FUSION_METHOD)
            c2 = fuseCoeff(cooef1[i][1], cooef2[i][1], FUSION_METHOD)
            c3 = fuseCoeff(cooef1[i][2], cooef2[i][2], FUSION_METHOD)
            fusedCooef.append((c1,c2,c3))
    # Third: After we fused the cooefficent we nned to transfor back to get the image
    fusedImage = pywt.waverec2(fusedCooef, wavelet)
    # Forth: normmalize values to be in uint8
    fusedImage = np.multiply(np.divide(fusedImage - np.min(fusedImage),(np.max(fusedImage) - np.min(fusedImage))),255)
    fusedImage = fusedImage.astype(np.uint8)
    # Fith: Save image
    length = len(str(image_objects_list[0]))
    filename = str(image_objects_list[0])
    filelocation = 'static/images/' + filename[:length-4] + '_wavelet.png'
    cv2.imwrite(filelocation,fusedImage)

@login_required
def image_fusion(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        image_objects_list = []
        checked_images_id = request.POST.getlist('image_checkbox')
        print('ID of checked images : ' + str(checked_images_id)) 
        if checked_images_id:
            print('Some Images or All Images') 
            for i in checked_images_id:
                image_object = UploadedImages.objects.get(id=i)
                image_objects_list.append(image_object.images)
            # print(image_objects_list) 
            # avg_min_max(request, image_objects_list)
            wavelet(request, image_objects_list)
            username = request.user
            email = request.user.email
            fused_images_max = ImageFusionUploadedImages.objects.filter(email=email, username=username).order_by('-id')[0]
            fused_images_min = ImageFusionUploadedImages.objects.filter(email=email, username=username).order_by('-id')[1]
            fused_images_avg = ImageFusionUploadedImages.objects.filter(email=email, username=username).order_by('-id')[2]
            all_images = UploadedImages.objects.filter(email=email, username=username)
            content = {
                "fused_image": True, 
                'all_images': all_images,
                'fused_images_max': fused_images_max,
                'fused_images_min': fused_images_min,
                'fused_images_avg': fused_images_avg
            }
            return render(request, 'home_app/image_processing.html', content)
        else:
            print('Empty') #
            return redirect('/image_processing')