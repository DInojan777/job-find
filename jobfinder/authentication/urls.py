from django.urls import path
from . import views

urlpatterns = [

    path('registerJobSeeker', views.RegisterJobSeeker.as_view(), name='registerJobSeeker'),
    path('registerClientAndContractor', views.RegisterClientAndContractor.as_view(), name='registerClientAndContractor'),
    path('memberLoginUsingPassword', views.MemberLoginUsingPassword.as_view(), name='memberLoginUsingPassword'),
    path('sendOtp', views.SendOtp.as_view(), name='sendOtp'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('cangePasswordApi', views.ChangePasswordApi.as_view(), name='changePasswordApi'),


    ]