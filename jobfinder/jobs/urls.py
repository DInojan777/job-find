from django.urls import path
from . import views

urlpatterns = [
    path('createJob', views.CreateJobDetails.as_view(), name='createJob'),
    path('jobListing', views.JobListing.as_view(), name='jobListing'),

]