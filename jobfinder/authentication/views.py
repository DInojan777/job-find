from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAuthentication
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .response_serializers import *
from .request_serializers import *
from users.models import *
from .model_helper import *
from django.contrib.auth import authenticate, login
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now




class RegisterJobSeeker(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
      data = request.data
      generatedPassword=data.get('password')

      username = data['email']
      #################################
      ## Valdating If user with same email or mobile number Already Exist
      #################################
      if User.objects.filter(username=username).exists():
            return Response(get_validation_failure_response("job seekser with this email already exists"))
      if getuser_by_mobile(data['mobile_number']) is not None:
            return Response(get_validation_failure_response(None, "Job seeker with mobile number already exist"))

      #################################
      ## Creating New User
      #################################
      user = User(username=data['email'], email=data['email'])
      user.first_name = data['first_name']
      user.last_name = data['last_name']
      user.set_password(generatedPassword)
      user.save()

      #################################
      ## Creating User Personal Detail
      #################################
      data_user={}
      data_user['gender']=data['gender']
      data_user['mobile_number']=data['mobile_number']
      userPersonalInfo=UserPersonalInfo.objects.create(user=user,**data_user)
      userPersonalInfo.save()

      #################################
      ## Creating Authentication
      #################################
      userAuthentication=UserAuthentication.objects.create(user=user)
      userAuthentication.is_job_seeker=True
      userAuthentication.is_active=True
      userAuthentication.save()

      #################################
      ## Creating Company - For Each User
      #################################
      company_meta={}
      company_meta['brand_name']='job seeker company'
      company_meta['display_name']='job seeker company'
      company_meta['type_is_provider']=False
      company_meta['is_active']=True
      companyMetaInfo=CompanyMeta.objects.create(**company_meta)
      companyMetaInfo.save()

      userDesignation=UserDesignation.objects.create(
            company=companyMetaInfo, name=userAuthentication.admin_registration_designation , is_admin=True)
      
      employee_id = random.randint(1000, 9999)
      form_employee_company_info = {}
      form_employee_company_info['employee_id'] = employee_id

      EmployeeCompanyInfo.objects.create(
            user=user, designation=userDesignation, company=companyMetaInfo, authentication=userAuthentication, **form_employee_company_info)

      token=get_user_token(user.username)

      response={'success':True,'token':token,'message':"Job seeker Registered Successfully"}

      return Response (get_success_response("Job seeker Registered Successfully",details=response))
    
# ========================================================================================================================

class RegisterClientAndContractor(APIView):
      
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        generatedPassword=data.get('password')
        username = data['email']
        if User.objects.filter(username=username).exists():
             return Response(get_validation_failure_response("job seekser with this email already exists"))
        if getuser_by_mobile(data['mobile_number_01']) is not None:
                    return Response(get_validation_failure_response(None, "Job seeker with mobile number already exist"))
        
        user = User(username=data['email'], email=data['email'],password=generatedPassword)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.set_password(generatedPassword)
        user.save()

        company_meta={}
        company_meta['brand_name']=data['brand_name']
      #   company_meta['display_name']=data['display_name']
      #   company_meta['type_is_provider']=data['type_is_provider']
        company_meta['is_active']=True
        companyMetaInfo=CompanyMeta.objects.create(**company_meta)
        companyMetaInfo.save()

        company_cont={}
        company_cont['address_id']=data['address_id']
        company_cont['mobile_number_01']=data['mobile_number_01']
      #   company_cont['communication_address']=data['communication_address']
      #   company_cont['city']=data['city']
      #   company_cont['district']=data['district']
      #   company_cont['state']=data['state']
      #   company_cont['pincode']=data['pincode']
      #   company_cont['country']=data['country']
        companyContactInfo=CompanyContactInfo.objects.create(**company_cont)
        companyContactInfo.save()

        form_company_branch = {}
        form_company_branch['name'] = company_meta['brand_name']
      #   form_company_branch['display_name'] = company_meta['brand_name']
        form_company_branch['is_parent'] = True
        form_company_branch['is_active'] = True
        companyBranchInfo=CompanyBranchInfo.objects.create(
              company= companyMetaInfo, company_contact=companyContactInfo, **form_company_branch)

        auth_info={}
        auth_info['is_client']=data['is_client']
        auth_info['is_contractor']=data['is_contractor']
        userAuthentication=UserAuthentication.objects.create(
              user=user, **auth_info)
        userAuthentication.is_active=True
        userAuthentication.is_job_seeker=False
        userAuthentication.save()

        user_personal_info={}
        user_personal_info['gender']=data['gender']
        user_personal_info['mobile_number']=data['mobile_number']
        user_personal_info['dob']=data['dob']
        UserPersonalInfo.objects.create(
              user=user, authentication=userAuthentication, **user_personal_info)

        userDesignation=UserDesignation.objects.create(
               company=companyMetaInfo, company_branch=companyBranchInfo, name=userAuthentication.admin_registration_designation , is_admin=True)
        
        employee_id = random.randint(1000, 9999)
        form_employee_company_info = {}
        form_employee_company_info['employee_id'] = employee_id

        EmployeeCompanyInfo.objects.create(
              user=user, designation=userDesignation, company=companyMetaInfo, company_branch=companyBranchInfo, authentication=userAuthentication, **form_employee_company_info)

        token=get_user_token(user.username)

        response={'success':True,'token':token,'message':" Registered Successfully"}

        return Response (get_success_response(" Registered Successfully",details=response))
    
# ========================================================================================================================

    
class MemberLoginUsingPassword(APIView):
      
      authentication_classes=[]
      permission_classes=[]

      def post(self,request,format=None):

            data=request.data
            email = data.get('email', None)
            mobile_number = data.get('mobile_number', None)
            password = data.get('password', None)
    
            if not password:
                 return Response(get_validation_failure_response([],"Password is required"))

            if not email and not mobile_number:
                  return Response(get_validation_failure_response([], "Mobile number or email is required"))
          
            user = None

            # Email login
            if email:
                  user = User.objects.filter(email=email.lower()).first()

            # Mobile login
            elif mobile_number:
                  userPersonalInfo = UserPersonalInfo.objects.filter(mobile_number=mobile_number).first()
                  if userPersonalInfo:
                        user = userPersonalInfo.user

            else:
                  return Response(get_validation_failure_response([], "Invalid user"))
            
            employeeCompanyInfo = EmployeeCompanyInfo.objects.filter(user=user).first()

            if not user.check_password(password):
                  return Response(get_validation_failure_response([], "Invalid user 1 credentials"))
            
            if employeeCompanyInfo and not employeeCompanyInfo.is_active:
                  return Response(get_validation_failure_response([], "Your account is deactivated. Please contact your administrator."))

            if employeeCompanyInfo and not employeeCompanyInfo.company.is_active:
                  return Response(get_validation_failure_response([], "Your account activation is in progress. You will receive an email notification upon activation."))

            if user is not None:
                  login(request, user)
                  token=Token.objects.get(user=user).key
                  EmployeeCompanyInfo.objects.get(user = user)
                    
                  employeeCompanyInfo.custom_field['variant'] = 'admin'
                  employeeCompanyInfo.save()

                  return Response(get_success_response(message="LoggedIn Successfully",details={"token":token}))
                    
            else:

                  return Response(get_validation_failure_response([], "Invalid Login Credentials"))
            

# ========================================================================================================================

# send an OTP to user's mobile or email
class SendOtp (APIView):

      authentication_classes=[]
      permission_classes=[]

      def post(self,request,format=None):

            data=request.data
            email = data.get('email', None)
            mobile_number = data.get('mobile_number', None)
            password = data.get('password', None)

            if not password:
                 return Response(get_validation_failure_response([],"Password is required"))

            if not email and not mobile_number:
                  return Response(get_validation_failure_response([], "Mobile number or email is required"))
          
            user = None
            # Email login
            if email:
                  user = User.objects.filter(email=email.lower()).first()
            # Mobile login
            elif mobile_number:     
                  userPersonalInfo = UserPersonalInfo.objects.filter(mobile_number=mobile_number).first()
                  user = userPersonalInfo.user
            else:
                  return Response(get_validation_failure_response([], "Invalid user"))
            
            employeeCompanyInfo = EmployeeCompanyInfo.objects.filter(user=user).first()

            if user.password != data["password"]:
                  otp = str((random.randint(1000,9999)))
                  authentication = employeeCompanyInfo.authentication
                  authentication.mobile_otp = otp
                  authentication.otp_expiry = timezone.now() + timedelta(minutes=2)  
                  authentication.save()
                  
                  if email:
                        token=Token.objects.get(user=user).key
                        return Response(get_success_response(message="OTP sent successfully to your email", details={"otp": otp,"token":token}))

                  # send OTP via SMS or email
                  elif mobile_number:
                        token=Token.objects.get(user=user).key
                        return Response(get_success_response(message="OTP sent successfully to your mobile number", details={"otp": otp,"token":token}))

            else:
                  return Response(get_validation_failure_response([], "Invalid user"))

# ========================================================================================================================


class Dashboard(APIView):
    
      authentication_classes = [authentication.TokenAuthentication]
      permission_classes = [permissions.IsAuthenticated]

      def post(self, request, format=None):

            data = request.data
            request_info = get_user_company_from_request(request)

            if request_info['company_info'] is not None:
                  print("request_info['company_info']=========>",request_info['company_info'])

                  try:
                        employeeCompanyInfo = EmployeeCompanyInfo.objects.get(
                        user=request_info['user'])

                        if employeeCompanyInfo.authentication.is_active == False:
                              return Response(get_validation_failure_response(None, 'Please login to continue'))
                        
                  except Exception as e:
                        return Response(get_validation_failure_response(None, 'Please login to continue'))
                  
                  res = get_success_response()
                  res["success"] = True

                  user_details = {}
                  user_details["employee_id"] = employeeCompanyInfo.id
                  user_details["name"] = employeeCompanyInfo.user.first_name
                  user_details["email"] = employeeCompanyInfo.user.email
                  user_details["is_active"] = employeeCompanyInfo.authentication.is_active
                  userPersonalInfo = UserPersonalInfo.objects.get(user=request_info['user'])
                  user_details["mobile_number"] = userPersonalInfo.mobile_number
                  user_details["gender"] = userPersonalInfo.gender

                  permission_details = {}
                  permission_details["is_admin"] = request_info['is_admin']
                  permission_details["is_contractor"] = request_info['is_contractor']
                  permission_details["is_client"] = request_info['is_client']
                  permission_details['is_job_seeker']=request_info['is_job_seeker']
                  permission_details["is_guest"] =request_info['is_guest']
                  permission_details["company_branch"] =request_info['company_branch']
                  permission_details["company_info"] = request_info['company_info'].id

                  dashboard={"user_details": user_details,
                        "permission_details": permission_details}                        
                  print("details=====================",dashboard)
                  return Response(get_success_response(message="your dashboard is",details=dashboard))
            else:
                  details = {}
                  print("details2")
                  print(details)
                  return Response(get_validation_failure_response(None, '2Please login to continue'))
            
# ========================================================================================================================
            

class ChangePasswordApi(APIView):
      
      authentication_classes=[]
      permission_classes=[]

      def post(self, request, format=None):

            data = request.data

            email = data.get("email", None)
            otp = data.get("otp", None)
            new_password = data.get("new_password", None)

            if email is not None:
                  user = User.objects.filter(email=email).first()
                  if otp is not None:
                        employeeCompanyInfo = EmployeeCompanyInfo.objects.get(user=user)
                        if employeeCompanyInfo.authentication.mobile_otp == otp:
                              if new_password is not None:
                                    user.set_password(new_password)
                                    user.save()
                                    return Response(get_success_response("password updated succesfully"))
                              else:
                                    return Response(get_validation_failure_response("Password is required"))
                        else:
                              return Response(get_validation_failure_response("otp is invalid"))

                  else:
                       return Response(get_validation_failure_response("otp is required"))
            else:
                  return Response(get_validation_failure_response("email is required"))