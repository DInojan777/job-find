from django.urls import path
from . import views

urlpatterns = [

    path('regiterUser', views.RegiterUser.as_view(), name='regiterUser'),
    ]