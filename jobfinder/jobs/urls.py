from django.urls import path
from . import views

urlpatterns = [
    path('createJob', views.CreateJob.as_view(), name='createJob'),
    path('GetJobList', views.GetJobList.as_view(), name='GetJobList'),

]