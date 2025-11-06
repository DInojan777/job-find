from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from authentication.response_serializers import *
from .serializers import *

class CreateJob(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        provider_id = data.get('provider_info_id')

        if not provider_id:
            return Response(get_validation_failure_response("Please provide provider_info_id"))

        try:
            EmployeeCompanyInfo.objects.get(id=provider_id)
        except EmployeeCompanyInfo.DoesNotExist:
            return Response(get_validation_failure_response("Invalid provider_info_id"))

        crt_job={}
        crt_job['provider_info_id']=data['provider_info_id']
        crt_job['description']=data['description']
        crt_job['vacancies']=data['vacancies']
        crt_job['reference_no']=data['reference_no']
        crt_job['budget']=data['budget']
        crt_job['expried_date']=data['expried_date']

        job_cont={}
        job_cont['mobile_number_01']=data['mobile_number_01']
        job_cont['address_line_01']=data['address_line_01']
        job_cont['communication_address']=data['communication_address']
        job_cont['city']=data['city']
        job_cont['district']=data['district']
        job_cont['state']=data['state']
        job_cont['pincode']=data['pincode']
        job_cont['country']=data['country']

        jobContactInfo=JobLocationInfo.objects.create(**job_cont)

        Joblist.objects.create(**crt_job,location=jobContactInfo)

        return Response(get_success_response(message="successfully job post"))

class GetJobList(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        joblist=Joblist.objects.all()
        res=GetJobListSerilizers(joblist, many=True).data

        return Response(get_success_response("joblisting",details=res))

