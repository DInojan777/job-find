from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAuthentication
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .response_serializers import *
from users.models import *
from .model_helper import *

class RegiterUser(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        username = data['email']
        if User.objects.filter(username=username).exists():
             return Response(get_validation_failure_response("User with this email already exists"))
        if getuser_by_mobile(data['mobile_number']) is not None:
                    return Response(get_validation_failure_response(None, "User with mobile number already exist"))

        user = User(username=data['email'], email=data['email'], password=data['email']+'@123')
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        data_user={}
        data_user['gender']=data['gender']
        data_user['mobile_number']=data['mobile_number']
        userPersonalInfo=UserPersonalInfo.objects.create(user=user,**data_user)
        userPersonalInfo.save()

        user_authe={}
        user_authe['is_client']=data['is_client']
        user_authe['is_contractor']=data['is_contractor']
        user_authe['is_job_seeker']=data['is_job_seeker']
        userAuthentication=UserAuthentication.objects.create(user=user,**user_authe)
        userAuthentication.is_active=True
        userAuthentication.save()

        token=get_user_token(user.username)

        response={'success':True,'token':token,'message':"User Registered Successfully"}
        
        return Response (get_success_response("User Registered Successfully",details=response))