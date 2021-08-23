from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_images/', views.upload_images, name='upload_images'),
    # path('login/', views.login, name='login'),
]