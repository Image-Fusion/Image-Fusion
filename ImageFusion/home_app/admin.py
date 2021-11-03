from django.contrib import admin
from . models import UploadedImages, ImageFusionUploadedImages

# Register your models here.
@admin.register(UploadedImages)
class UploadedImagesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


@admin.register(ImageFusionUploadedImages)
class ImageFusionUploadedImagesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')