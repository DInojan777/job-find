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
from django.contrib.auth import authenticate, login


class RegisterJobSeeker(APIView):

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
    
class RegisterClientAndContractor(APIView):
      
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        username = data['email']
        if User.objects.filter(username=username).exists():
             return Response(get_validation_failure_response("job seekser with this email already exists"))
        if getuser_by_mobile(data['mobile_number_01']) is not None:
                    return Response(get_validation_failure_response(None, "Job seeker with mobile number already exist"))
        
        user = User(username=data['email'], email=data['email'])
        user.password=data['password']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        company_meta={}
        company_meta['brand_name']=data['brand_name']
        company_meta['display_name']=data['display_name']
        company_meta['type_is_provider']=data['type_is_provider']
        company_meta['is_active']=True
        companyMetaInfo=CompanyMeta.objects.create(**company_meta)
        companyMetaInfo.save()

        company_cont={}
        company_cont['address_id']=data['address_id']
        company_cont['mobile_number_01']=data['mobile_number_01']
        company_cont['communication_address']=data['communication_address']
        company_cont['city']=data['city']
        company_cont['district']=data['district']
        company_cont['state']=data['state']
        company_cont['pincode']=data['pincode']
        company_cont['country']=data['country']
        companyContactInfo=CompanyContactInfo.objects.create(**company_cont)
        companyContactInfo.save()

        form_company_branch = {}
        form_company_branch['name'] = company_meta['brand_name']
        form_company_branch['display_name'] = company_meta['brand_name']
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
    

    
class MemberLoginUsingPassword(APIView):
      
      authentication_classes=[]
      permission_classes=[]

      def post(self,request,format=None):
            data=request.data
            email = data.get('email', None)
            mobile_number = data.get('mobile_number', None)
            password = data.get('password', None)

            print("data================>",data)
            if not password:
                 return Response(get_validation_failure_response([],"Password is required"))
            print("received password ============>",password)
            if not email and not mobile_number:
                  print("+++++++++++++++++++++++++++++++")
                  return Response(get_validation_failure_response([], "Mobile number or email is required"))
            print("---------------------------------")
          
            user = None
            # Email login
            if email:
                  user = User.objects.filter(email=email.lower()).first()
                  print("received email ============>", email, "user==========>", user)
            # Mobile login
            elif mobile_number:
                  upi = UserPersonalInfo.objects.filter(mobile_number=mobile_number).first()
                  if upi:
                        user = upi.user
                  print("received number ============>", mobile_number, "user==========>", user)
            else:
                  return Response(get_validation_failure_response([], "Invalid user"))

            if user.password != data["password"]:
                  print("*********************** password mismatched *************************")
                  return Response(get_validation_failure_response([], "Invalid user credentials"))
            
            emp_info = EmployeeCompanyInfo.objects.filter(user=user).first()
            if emp_info and not emp_info.is_active:
                  print("############################")
                  return Response(get_validation_failure_response([], "Your account is deactivated. Please contact your administrator."))

            if emp_info and not emp_info.company.is_active:
                  return Response(get_validation_failure_response([], "Your account activation is in progress. You will receive an email notification upon activation."))

            token=Token.objects.get(user=user).key
            print("=========================================pass=========")
            return Response(get_success_response(message="password matched",details=token))



