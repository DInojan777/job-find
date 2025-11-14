from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from authentication.response_serializers import *
from .serializers import *
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.utils.dateparse import parse_datetime

class CreateJob(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        provider_id = data.get('provider_info_id')

        if not provider_id:
            return Response(get_validation_failure_response("Please provide provider_info_id"))
        try:
            employeeCompanyInfo=EmployeeCompanyInfo.objects.get(id=provider_id)
        except EmployeeCompanyInfo.DoesNotExist:
            return Response(get_validation_failure_response("Invalid provider_info_id"))
        user=employeeCompanyInfo.user

        crt_job={}
        crt_job['provider_info_id']=data['provider_info_id']
        crt_job['position']=data['position']
        crt_job['description']=data['description']
        crt_job['experience']=data['experience']
        crt_job['reference_name']=data['reference_name']
        crt_job['reference_no']=data['reference_no']
        crt_job['vacancies']=data['vacancies']
        crt_job['budget']=data['budget']
        crt_job['expried_date']=data['expried_date']

        job_cont={}
        job_cont['mobile_number_01']=data['mobile_number_01']
        job_cont['address_line_01']=data['address_line_01']
        job_cont['city']=data['city']
        job_cont['district']=data['district']
        job_cont['state']=data['state']
        job_cont['pincode']=data['pincode']
        job_cont['country']=data['country']

        jobContactInfo=JobLocationInfo.objects.create(**job_cont)

        Joblist.objects.create(**crt_job,location=jobContactInfo,raised_by=user)

        return Response(get_success_response(message="successfully job post"))

# ========================================================================================================================


class GetJobList(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print("data==========>",data)

        now= timezone.now()        
        queryset = Joblist.objects.filter(expried_date__gt=now)

        search= data.get('search')
        if search:
            queryset = queryset.filter(Q(description__icontains=search) | Q(position__icontains=search))

        recent_days = data.get('recent_days')
        if recent_days is not None:
            recent_days = int(recent_days)
            recent_cutoff = now - timedelta(days=recent_days)
            queryset = queryset.filter(created_at__gte=recent_cutoff)
        
        experience=data.get('exprience')
        if experience is not None:
            queryset=queryset.filter(experience_contains=experience)
        
        address_line_01=data.get('address_line_01')
        if address_line_01 is not None:
            queryset = queryset.filter(location__address_line_01__icontains=address_line_01)
        city=data.get('city')
        if city is not None:
            queryset = queryset.filter(location__city__icontains=city)
        district=data.get('district')
        if district is not None:
            queryset = queryset.filter(location__district__icontains=district)

        start_date = data.get('start_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        end_date = data.get('end_date')
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        if queryset is not None:
            serializer = GetJobListSerializer(queryset, many=True)
            print(serializer.data)

            return Response(get_success_response(details=serializer.data))
        else:
            return Response(get_validation_failure_response('not found'))
        

# ========================================================================================================================
        

class ApplyJob(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, formate=None):
        data=request.data    

        job_id = data.get('job_id')
        applicant_details_id=data.get('applicant_details_id')

        if not job_id:
            return Response(get_validation_failure_response("Please provide job_id"))
        try:
            joblist=Joblist.objects.get(id=job_id)
        except Joblist.DoesNotExist:
            return Response(get_validation_failure_response("Invalid job_id"))
        
        if not applicant_details_id:
            return Response(get_validation_failure_response("Please provide applicant_details_id"))
        try:
            employeeCompanyInfo=EmployeeCompanyInfo.objects.get(id=applicant_details_id)
        except EmployeeCompanyInfo.DoesNotExist:
            return Response(get_validation_failure_response("Invalid applicant_details_id"))
        
        job_app={}
        job_app['job_id']=data['job_id']
        job_app['applicant_details_id']=data['applicant_details_id']
        job_app['expection_rate']=data['expection_rate']
        # job_app['status']=data['status']

        JobApplication.objects.create(**job_app)

        return Response(get_success_response('Job apply successfully'))
    
    
# ========================================================================================================================


class GetJobApplicaten(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, formate=None):
        data= request.data

        job_id=data.get('job_id')

        if not job_id:
            return Response(get_validation_failure_response("Please provide job_id"))
        try:
            jobApplication=JobApplication.objects.filter(job__id=job_id)
        except JobApplication.DoesNotExist:
            return Response(get_validation_failure_response("Invalid job_id"))
        
        serializers=GetApplyedJobSerializer(jobApplication, many=True).data
        return Response(get_success_response(details=serializers))