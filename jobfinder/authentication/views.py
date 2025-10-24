from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAuthentication
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .response_serializers import *
from .request_serializers import *
from users.models import *
from .model_helper import *

class RegiterJobSeeker(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        username = data['email']
        if User.objects.filter(username=username).exists():
             return Response(get_validation_failure_response("job seekser with this email already exists"))
        if getuser_by_mobile(data['mobile_number']) is not None:
                    return Response(get_validation_failure_response(None, "Job seeker with mobile number already exist"))

        user = User(username=data['email'], email=data['email'])
        user.password=data['password']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        data_user={}
        data_user['gender']=data['gender']
        data_user['mobile_number']=data['mobile_number']
        userPersonalInfo=UserPersonalInfo.objects.create(user=user,**data_user)
        userPersonalInfo.save()

        userAuthentication=UserAuthentication.objects.create(user=user)
        userAuthentication.is_job_seeker=True
        userAuthentication.is_active=True
        userAuthentication.save()

        token=get_user_token(user.username)

        response={'success':True,'token':token,'message':"Job seeker Registered Successfully"}

        return Response (get_success_response("Job seeker Registered Successfully",details=response))
    
# class RegiterClientAndContractor(APIView):
      
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request, format=None):
#         data = request.data
        
#         validateRequest=ValidateRequest(
#               request=request, request_serializer=RegisterCompanySerializer)
        