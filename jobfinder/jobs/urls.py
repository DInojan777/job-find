from django.urls import path
from . import views

urlpatterns = [
    path('createJob', views.CreateJob.as_view(), name='createJob'),
    path('jobListing', views.JobListing.as_view(), name='jobListing'),

]