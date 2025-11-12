from django.db import models
from authentication.models import BaseModelMixin
from users.models import EmployeeCompanyInfo
from django.contrib.auth.models import User
from authentication.models import *
from company.models import *
from multiselectfield import MultiSelectField

class JobDocument(BaseModelMixin):

    title = models.CharField(max_length=220, null=True, blank=True)
    photo = models.ImageField(upload_to='job_document', null=True, blank=True)
    time_stamp = models.DateTimeField(default=now, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.FileField(upload_to='job_document',null=True,blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        title = str(self.id)+"==="+str(self.time_stamp)
        return title

class JobLocationInfo(BaseModelMixin):
    is_default = models.BooleanField(default=True)
    address_id = models.CharField(max_length=30, null=True, blank=True)
    address_line_01 = models.CharField(max_length=70, null=True, blank=True)
    mobile_number_01 = models.CharField(max_length=20, null=True, blank=True)
    mobile_number_02 = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    google_place_link = models.CharField(max_length=220, null=True, blank=True)

class Joblist(BaseModelMixin):

    SALARY_CHOICES = [
        ('monthly', 'Monthly wages'),
        ('daily', 'Daily wages'),
        ('hourly', 'Hourly wages'),
        ('contractor', 'Contactor-based'),

    ]
    raised_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    provider_info=models.ForeignKey(EmployeeCompanyInfo, on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=225,null=True, blank=True)
    description=models.CharField(max_length=225, null=True, blank=True)
    experience = models.IntegerField(default=0)
    reference_name = models.CharField(max_length=210, null=True, blank=True)
    reference_no=models.CharField(max_length=8, null=True, blank=True)
    vacancies=models.CharField(max_length=8, null=True, blank=True)
    budget=models.CharField(max_length=15, null=True, blank=True)
    payment_type = MultiSelectField(max_length=100, choices=SALARY_CHOICES, blank=True, default='')
    expried_date = models.DateTimeField(null=True)
    location=models.ForeignKey(JobLocationInfo, on_delete=models.CASCADE, null=True, blank=True)
    attachments =models.ManyToManyField(JobDocument)

