from rest_framework import serializers
from .models import *

class GetJobListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Joblist
        fields='__all__'

class GetApplyedJobSerializer(serializers.ModelSerializer):

    user_applicant_details= serializers.SerializerMethodField()

    class Meta:
        model=JobApplication
        fields=['job', 'applicant_details', 'expection_rate','user_applicant_details']

    def get_user_applicant_details(self, obj):
        return{"user":obj.applicant_details.user.username, "is_job_seeker":obj.applicant_details.authentication.is_job_seeker, 
               "is_client":obj.applicant_details.authentication.is_client,"is_contractor":obj.applicant_details.authentication.is_contractor}
