from django.contrib import admin
from . models import UploadedImages

# Register your models here.
@admin.register(UploadedImages)
class UploadedImagesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')