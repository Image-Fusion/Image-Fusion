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
from PIL import Image # pip install Pillow
import numpy as np # pip install numpy
from django.core.files.storage import default_storage
import base64
import pywt # pip install PyWavelets
import cv2 # pip install opencv-python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import argparse

from .GCF import GC
from .focus_maps import focus_maps
from .morphological import morphological_transform
from .median import median_filter

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
            # Image Size {Single Value for Single Band Image(eg. Grayscale Image) and Tuple for Multi Band Image(eg. RGB Image)}
            image_size_1           = img_1.size
            image_size_2           = img_2.size
            width_1, height_1      = img_1.size
            new_size               = (width_1, height_1)
            img_avg                = Image.new(mode="L", size=new_size)
            img_min                = Image.new(mode="L", size=new_size)
            img_max                = Image.new(mode="L", size=new_size)
            image_size_avg         = img_avg.size
            image_size_min         = img_min.size
            image_size_max         = img_max.size
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
                # print("Task completed")
                username   = request.user
                email      = request.user.email
                path_img_1 = 'static/temporary/images/'+'input_img_1'+'.png'
                path_img_2 = 'static/temporary/images/'+'input_img_2'+'.png'
                path_avg   = 'static/temporary/images/'+'avg'+'.png'
                path_min   = 'static/temporary/images/'+'min'+'.png'
                path_max   = 'static/temporary/images/'+'max'+'.png'
                img_1.save(path_img_1)
                img_2.save(path_img_2)
                img_avg.save(path_avg) 
                img_min.save(path_min) 
                img_max.save(path_max)
                return True
            else:
                return False
            # for i in [path_avg, path_min, path_max]:
            #     print(i)
            #     print(":::")
            #     ImageFusionUploadedImages.objects.create(username=username, email=email, images=i)

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
    with Image.open('static/images/' + str(image_objects_list[0])) as img_1:
        with Image.open('static/images/' + str(image_objects_list[1])) as img_2:
            path_img_1 = 'static/temporary/images/'+'input_img_1'+'.png'
            path_img_2 = 'static/temporary/images/'+'input_img_2'+'.png'
            img_1.save(path_img_1)
            img_2.save(path_img_2)
            input_img_width, input_img_height = img_1.size
    # Params
    FUSION_METHOD = 'mean' # Can be 'min' || 'max || anything you choose according theory
    # Read the two image
    I1               = cv2.imread('static/images/' + str(image_objects_list[0]),0)
    I2               = cv2.imread('static/images/' + str(image_objects_list[1]),0)
    image_I1_size    = (input_img_width, input_img_height)
    # We need to have both images the same size
    I2 = cv2.resize(I2,I1.shape) # Do this because we used two random images
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
            c1 = fuseCoeff(cooef1[i][0],cooef2[i][0], FUSION_METHOD)
            c2 = fuseCoeff(cooef1[i][1], cooef2[i][1], FUSION_METHOD)
            c3 = fuseCoeff(cooef1[i][2], cooef2[i][2], FUSION_METHOD)
            fusedCooef.append((c1,c2,c3))
    # Third: After we fused the cooefficent we nned to transfor back to get the image
    fusedImage = pywt.waverec2(fusedCooef, wavelet)
    # Forth: normmalize values to be in uint8
    fusedImage = np.multiply(np.divide(fusedImage - np.min(fusedImage),(np.max(fusedImage) - np.min(fusedImage))),255)
    fusedImage = fusedImage.astype(np.uint8)
    fusedImage = cv2.resize(fusedImage,image_I1_size)
    # Fith: Save image
    length = len(str(image_objects_list[0]))
    filename = str(image_objects_list[0])
    # filelocation = 'static/images/'+ filename[:length-4] + '_wavelet.png'
    filelocation = 'static/temporary/images/' + 'wavelet.png'
    cv2.imwrite(filelocation,fusedImage)

def show_rgb_img(img):
    """Convenience function to display a typical color image"""
    # return plt.imshow(cv2.cvtColor(img, cv2.CV_32S))
    plt.savefig('static/temporary/images/color.png', bbox_inches='tight')
    input_img_1 = mpimg.imread('static/images/' + str(image_objects_list[0]),0)
    input_img_2 = mpimg.imread('static/images/' + str(image_objects_list[1]),0)
    mpimg.imsave("color_input_img_1.png", input_img_1)
    mpimg.imsave("color_input_img_2.png", input_img_2)

def to_gray(color_img):
    print("to_gray")
    gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    print(gray)
    mpimg.imsave("gray.png", gray)
    return gray

def gen_sift_features(gray_img):
    # sift = cv2.xfeatures2d.SIFT_create()
    # kp is the keypoints
    #
    # desc is the SIFT descriptors, they're 128-dimensional vectors
    # that we can use for our final features
    # kp, desc = sift.detectAndCompute(gray_img, None)
    sift = cv2.SIFT_create() 
    kp, desc = sift.detectAndCompute(gray_img, None)
    return kp, desc

def show_sift_features(gray_img, color_img, kp):
    store = cv2.drawKeypoints(gray_img, kp, color_img.copy())
    # save a image using extension
    im1 = store.save("sift_features.jpg")
    # return plt.imshow(store)

def GCF_image_fusion(request, image_objects_list):
    # Parameters
    color = False 
    m     = 1 # no. of times gc filter is applied
    p, q  = 7, 7 # dimension of patch in focus region
    n     = 5 # dilation and erosion kernel size nxn
    if color:
        im1 = cv2.imread('static/images/' + str(image_objects_list[0]))
        im2 = cv2.imread('static/images/' + str(image_objects_list[1]))
    else :
        im1 = cv2.imread('static/images/' + str(image_objects_list[0]), cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread('static/images/' + str(image_objects_list[1]), cv2.IMREAD_GRAYSCALE)
    igc1   = GC(im1, m, color)
    igc2   = GC(im2, m, color)
    f1     = im1 - igc1
    f2     = im2 - igc2
    c1, c2 = focus_maps(f1, f2, p, q, color)
    cn1    = morphological_transform(c1, n)
    cn2    = morphological_transform(c2, n)
    cm1    = median_filter(cn1, n)
    cm2    = median_filter(cn2, n)
    final1 = np.zeros(im1.shape)
    final2 = np.zeros(im2.shape)
    if color:
        for i in range(3):
            final1[:,:,i] = cm1*im1[:,:,i] + (1 - cm1)*im2[:,:,i]
            final2[:,:,i] = (1 - cm2)*im1[:,:,i] + cm2*im2[:,:,i]
    else:
        final1 = cm1*im1 + (1 - cm1)*im2
        final2 = (1 - cm2)*im1 + cm2*im2
    cv2.imwrite("static/temporary/images/gcf.png", final2.astype(int))

@login_required
def image_fusion(request, method):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        image_objects_list = []
        checked_images_id = request.POST.getlist('image_checkbox')
        # print('ID of checked images : ' + str(checked_images_id)) 
        if checked_images_id:
            # print('Some Images or All Images') 
            for i in checked_images_id:
                image_object = UploadedImages.objects.get(id=i)
                image_objects_list.append(image_object.images)
            # print(image_objects_list) 
            avg_min_max_result = False
            if method == 'avg_min_max':
                # Average, Min, Max
                avg_min_max_result = avg_min_max(request, image_objects_list)
            elif method == 'wavelet':
                # Wavelet
                wavelet(request, image_objects_list)
            elif method == 'sift_matching':
                # SIFT
                img_1      = cv2.imread('static/images/' + str(image_objects_list[0]),1)
                img_2      = cv2.imread('static/images/' + str(image_objects_list[1]),1)
                path_img_1 = 'static/temporary/images/'+'input_img_1'+'.png'
                path_img_2 = 'static/temporary/images/'+'input_img_2'+'.png'
                cv2.imwrite(path_img_1, img_1)
                cv2.imwrite(path_img_2, img_2)
                # to gray
                img_1_gray = to_gray(img_1)
                img_2_gray = to_gray(img_2)
                # generate SIFT keypoints and descriptors
                img_1_kp, img_1_desc  = gen_sift_features(img_1_gray)
                img_2_kp, img_2_desc  = gen_sift_features(img_2_gray)
                # create a BFMatcher object which will match up the SIFT features
                bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
                matches = bf.match(img_1_desc, img_2_desc)
                # Sort the matches in the order of their distance.
                matches = sorted(matches, key = lambda x:x.distance)
                # draw the top N matches
                N_MATCHES = 100
                match_img = cv2.drawMatches(
                    img_1, 
                    img_1_kp,
                    img_2, 
                    img_2_kp,
                    matches[:N_MATCHES], 
                    img_2.copy(), 
                    flags=0
                )
                plt.figure(figsize=(12,6))
                plt.imshow(match_img)
                plt.savefig('static/temporary/images/match_sift.png')

            elif method == 'gaussian_curvature_filter':
                # Gaussian Curvature Filter
                img_1      = cv2.imread('static/images/' + str(image_objects_list[0]),1)
                img_2      = cv2.imread('static/images/' + str(image_objects_list[1]),1)
                path_img_1 = 'static/temporary/images/'+'input_img_1'+'.png'
                path_img_2 = 'static/temporary/images/'+'input_img_2'+'.png'
                cv2.imwrite(path_img_1, img_1)
                cv2.imwrite(path_img_2, img_2)
                GCF_image_fusion(request, image_objects_list)

            username         = request.user
            email            = request.user.email
            all_images       = UploadedImages.objects.filter(email=email, username=username)
            content          = {
                "fused_image"              : True,
                'all_images'               : all_images,
                'avg_min_max'              : True if method == 'avg_min_max' else False,
                'avg_min_max_result'       : avg_min_max_result,
                'wavelet'                  : True if method == 'wavelet' else False,
                'sift_matching'            : True if method == 'sift_matching' else False,
                'gaussian_curvature_filter': True if method == 'gaussian_curvature_filter' else False
            }
            return render(request, 'home_app/image_processing.html', content)
        else:
            print('Empty')
            return redirect('/image_processing')