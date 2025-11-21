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
    description=models.TextField(null=True, blank=True)
    experience = models.IntegerField(default=0)
    reference_name = models.CharField(max_length=210, null=True, blank=True)
    reference_no=models.CharField(max_length=8, null=True, blank=True)
    vacancies=models.CharField(max_length=8, null=True, blank=True)
    budget=models.CharField(max_length=15, null=True, blank=True)
    payment_type = MultiSelectField(max_length=100, choices=SALARY_CHOICES, blank=True, default='')
    expried_date = models.DateTimeField(null=True)
    location=models.ForeignKey(JobLocationInfo, on_delete=models.CASCADE, null=True, blank=True)
    attachments =models.ManyToManyField(JobDocument)

class JobApplication(BaseModelMixin):

    job=models.ForeignKey(Joblist, on_delete=models.CASCADE, null=True, blank=True)
    applicant_details=models.ForeignKey(EmployeeCompanyInfo, on_delete=models.CASCADE, null=True, blank=True)
    expection_rate=models.CharField(max_length=21, null=True, blank=True)

class JobApplicationStatus(BaseModelMixin):

    APPLICANT_STATUS=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
    ]
    job=models.ForeignKey(Joblist, on_delete=models.CASCADE, null=True, blank=True)
    job_applicant=models.ForeignKey(JobApplication, on_delete=models.CASCADE, null=True, blank=True)
    status=models.CharField(max_length=200,choices=APPLICANT_STATUS, null=True, blank=True, default='pending')

class JobDetails(BaseModelMixin):
    job=models.ForeignKey(Joblist, on_delete=models.CASCADE, null=True, blank=True)
    jobApplicationStatus=models.ForeignKey(JobApplicationStatus, on_delete=models.CASCADE, null=True, blank=True)
    work_start_date=models.DateTimeField(null=True, blank=True)
    work_end_date=models.DateTimeField(null=True, blank=True)
    payment_details=models.CharField(max_length=220, null=True, blank=True)