from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_images/', views.upload_images, name='upload_images'),
    path('image_processing/', views.image_processing, name='image_processing'),
    path('delete_image/<str:pk>/', views.delete_image, name='delete-image'),
    path('delete_all_images/', views.delete_all_images, name='delete-all-images'),
    # path('login/', views.login, name='login'),
]