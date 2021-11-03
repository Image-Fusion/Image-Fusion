from django.db import models

# Create your models here.
class UploadedImages(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    images = models.ImageField()
    # text_base64 = models.CharField(blank=True)

    def __str__(self):
        return self.username + " " + self.email


class ImageFusionUploadedImages(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    images = models.ImageField()

    def __str__(self):
        return self.username + " " + self.email