from django.db import models
from authentication.models import BaseModelMixin
from users.models import EmployeeCompanyInfo
from django.contrib.auth.models import User
from authentication.models import *
from company.models import *

class JobDocument(BaseModelMixin):

    title = models.CharField(max_length=220, null=True, blank=True)
    photo = models.ImageField(upload_to='job_document', null=True, blank=True)
    time_stamp = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        title = str(self.id)+"==="+str(self.time_stamp) 
        return title

class JobLocationInfo(BaseModelMixin):
    is_default = models.BooleanField(default=True)
    address_id = models.CharField(max_length=30, null=True, blank=True)
    address_line_01 = models.CharField(max_length=70, null=True, blank=True)
    address_line_02 = models.CharField(max_length=70, null=True, blank=True)
    mobile_number_01 = models.CharField(max_length=20, null=True, blank=True)
    mobile_number_02 = models.CharField(max_length=20, null=True, blank=True)
    communication_address = models.CharField(
        max_length=220, null=True, blank=True)
    billing_address = models.CharField(max_length=220, null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    google_place_link = models.CharField(max_length=220, null=True, blank=True)

class Joblist(BaseModelMixin):

    description=models.CharField(max_length=220, null=True, blank=True)
    reference_no=models.CharField(max_length=8, null=True, blank=True)
    vacancies=models.CharField(max_length=8, null=True, blank=True)
    budget=models.CharField(max_length=15, null=True, blank=True)
    expried_date = models.DateTimeField(auto_now=True)
    location=models.ForeignKey(JobLocationInfo, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='job_document', null=True, blank=True)

class JobDetails(BaseModelMixin):

    provider_info=models.ForeignKey(EmployeeCompanyInfo, on_delete=models.CASCADE, null=True, blank=True)
    joblist=models.ManyToManyField(Joblist, null=True, blank=True)
