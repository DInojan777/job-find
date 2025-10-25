from django.urls import path
from . import views

urlpatterns = [

    path('registerJobSeeker', views.RegisterJobSeeker.as_view(), name='registerJobSeeker'),
    path('registerClientAndContractor', views.RegisterClientAndContractor.as_view(), name='registerClientAndContractor'),
    
    ]