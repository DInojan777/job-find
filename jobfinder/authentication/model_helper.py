from .models import *
from users.models import *
from rest_framework.authtoken.models import Token

def get_user_token(username):
    try:
        user=User.objects.get(username=username)
        try:
            token=Token.objects.get(user=user)
            return token.key
        except:
            token=Token.objects.create(user=user)
            return token.key
    except:
        return None

def get_active_user(**kargs):
    try:
        return UserAuthentication.objects.get(**kargs)
    except:
        return None

def getuser_by_mobile(username):
    try:
        ep = UserPersonalInfo.objects.get(mobile_number=username)
        return ep.user
    except:
        return None

def get_object_by_pk(model, pk):
    try:
        return model.objects.get(pk=pk)
    except:
        return None

def get_user_from_request(request_info, data):
    user = request_info['user']
    if 'user_id' in data:
        try:
            employeeCompanyInfo = get_object_by_pk(
                EmployeeCompanyInfo, data['user_id'])
            user = employeeCompanyInfo.user
        except:
            pass
    return user
    
def get_user_company_from_user(user):

    response = {
        "user": None,
        "company_info": None,
        "employee_id": None,
        "is_admin": False,
        'is_branch_admin': False,
        "is_super_admin": False,
        "is_client": False,
        "is_contractor": False,
        "is_job_seeker": False,
        'has_company': False,
        'company': None,
        'company_branch': None,
        'personal_info':None,
        'photo': None,
        'name': None,
        'mobile_number': None
    }
    try:
        response['user']=user
        user_auth=get_active_user(user=user)
        response['is_admin']=user_auth.is_active and user_auth.is_admin

        try:
            employee_company_info=EmployeeCompanyInfo.objects.get(
                user=user)
            response['company_info']=employee_company_info
            response['employee_id']=employee_company_info.id

            try:
                response['photo']=employee_company_info.photo.url
            except:
                pass

            response['name']=employee_company_info.user.username
            response['is_super_admin']=employee_company_info.authentication.is_super_admin
            response['is_client']=employee_company_info.authentication.is_client
            response['is_contractor']=employee_company_info.authentication.is_contractor
            response['is_job_seeker']=employee_company_info.authentication.is_job_seeker

            user_personal_info=UserPersonalInfo.objects.get(
                user=user)
            response['personal_info']=user_personal_info
            response['mobile_number']=user_personal_info.mobile_number

            try:
                response['is_branch_admin']=user_auth.is_active and employee_company_info.designation.is_admin
                response['designation'] = employee_company_info.designation.name
            except:
                pass

            response['has_company']=True
            response['company']={'name':employee_company_info.company.brand_name,'id':employee_company_info.company.id,
                                'type_is_provider':employee_company_info.company.type_is_provider}
            
        except Exception as e:
            response['has_company']=False
    except:
        pass
    return response

def get_user_company_from_request(request):
    response={
        "user":None,
        "company_info":None,
        "is_admin":False,
        "is_client":False,
        "is_contractor":False,
        "is_job_seeker":False
    }
    try:
        token=request.Meta.get('HTTP_AUTHORIZATION')
        token=token.replace("Token","")
        try:
            user=Token.objects.get(key=token).user
            response=get_user_company_from_user(user=user)
        except:
            pass
    except:
        pass
    return response

class ValidateRequest():

    def __init__(self, request, request_serializer= None):

        self.request=request
        self.request_data=request.data
        self.request_info=get_user_company_from_request(request)
        self.request_serializer=request_serializer

    def employee_company_info(self):
        return self.request_info['company_info']

    def employee_personal_info(self):
        employee_personal_info= UserPersonalInfo.objects.get(user=self.request_info['user'])
        print("employee_personal_info===========>",employee_personal_info.id)
        return employee_personal_info
    
    def is_admin(self):
        if self.is_valid():
            userAuthentication = UserAuthentication.objects.get(
                user=self.request_info['user'])
            return userAuthentication.is_admin
        return False
    
    def is_valid_user(self):
        if self.request_info['company_info']:
            return True
        else:
            return False
    
    def errors(self):
        return self.errors

    def is_valid(self):
        if self.is_valid_user() == False:
            return False
        elif self.request_serializer is not None:
            print("444", self.request_data)
            request_serializer_response = self.request_serializer(
                data=self.request_data)
            if request_serializer_response.is_valid() == True:
                return True
            else:
                self.errors = request_serializer_response.errors
                print("errors======", request_serializer_response.errors)
                return False
        else:
            return True
    
    def is_valid_open_request(self):
        if self.request_serializer is not None:
            print("444", self.request_data)
            request_serializer_response=self.request_serializer(data=self.request_data)
            if request_serializer_response.is_valid() == True:
                 print("35444", self.request_data)
                 return True
            else:
                print("5444", self.request_data)
                self.errors=request_serializer_response.errors
                print("errors======", request_serializer_response.errors)
        else:
            return False
        
    def errors_formatted(self):
        return "Invalid Request Info"