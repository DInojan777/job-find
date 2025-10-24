from django.urls import path
from . import views

urlpatterns = [

    path('regiterJobSeeker', views.RegiterJobSeeker.as_view(), name='regiterJobSeeker'),
    ]