from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from authentication.response_serializers import *
from .serializers import *

class CreateJobDetails(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        provider_info_id = data.get('provider_info_id')
        joblist_data = data.get('joblist', [])

        if not provider_info_id:
            return Response(get_validation_failure_response([], "provider_info_id is required"))
        if not joblist_data:
            return Response(get_validation_failure_response([], "joblist data is required"))

        try:
            provider_info = EmployeeCompanyInfo.objects.get(id=provider_info_id)
        except EmployeeCompanyInfo.DoesNotExist:
            return Response(get_validation_failure_response([], "Invalid provider_info_id"))

        jobDetails = JobDetails.objects.create(provider_info=provider_info)

        for job_item in joblist_data:
            location_data = job_item.get('location', {})

            jobLocationInfo = JobLocationInfo.objects.create(**location_data)

            crt_job = {
                'description': job_item.get('description'),
                'reference_no': job_item.get('reference_no'),
                'vacancies': job_item.get('vacancies'),
                'budget': job_item.get('budget'),
                'location': jobLocationInfo
            }

            joblist = Joblist.objects.create(**crt_job)
            jobDetails.joblist.add(joblist)

        return Response(get_success_response(message="Job details created successfully"))
    

class JobListing(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        joblist=Joblist.objects.all()
        res=GetJobListSerilizers(joblist, many=True).data
        return Response(get_success_response("joblisting",details=res))

