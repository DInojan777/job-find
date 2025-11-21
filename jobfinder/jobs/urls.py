from django.urls import path
from . import views

urlpatterns = [
    
    path('createJob', views.CreateJob.as_view(), name='createJob'),
    path('getJobList', views.GetJobList.as_view(), name='getJobList'),
    path('applyJob', views.ApplyJob.as_view(), name='applyJob'),
    # path('getJobApplicant', views.GetJobApplicant.as_view(), name='getJobApplicant'),
    path('addApplicationStatus', views.AddApplicationStatus.as_view(), name='addApplicationStatus'),
    path('getApplicationStatus', views.GetApplicationStatus.as_view(), name='getApplicationStatus'),
    path('addProtfolio', views.AddProtfolio.as_view(), name='addProtfolio'),

]