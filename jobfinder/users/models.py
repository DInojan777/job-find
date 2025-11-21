from django.db import models
from django.contrib.auth.models import User
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now
from company.models import *
from multiselectfield import MultiSelectField
class UserDesignation(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_job_seeker=models.BooleanField(default=False)

    def __str__(self):
        return str(self.name) +"===" +str(self.id)+"====="+str(self.code)

class UserPersonalInfo(BaseModelMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authentication=models.ForeignKey(UserAuthentication,on_delete=models.CASCADE,null=True, blank=True)
    gender = models.CharField(max_length=5)
    age = models.CharField(max_length=3,null=True,blank=True)
    aadhar = models.CharField(max_length=130, null=True, blank=True)
    address = models.CharField(max_length=130, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    dob = models.DateField(auto_now=False, null=True, blank=True)
    blood_group = models.CharField(max_length=70, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, unique=False, null=True, blank=True)

    def __str__(self):
        return self.user.first_name +"==="+ self.mobile_number+"==="+str(self.id)
    
class EmployeeCompanyInfo(BaseModelMixin):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=30, null=True, blank=True)
    designation =  models.ForeignKey(UserDesignation, on_delete=models.SET_NULL, null=True, blank=True)
    department =  models.ForeignKey(CompanyDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    date_of_joining = models.DateField(auto_now=False, null=True, blank=True)
    employment_type = models.CharField(max_length=40, null=True, blank=True)
    authentication = models.ForeignKey(UserAuthentication, on_delete=models.CASCADE, null=True, blank=True)
    referrer = models.ForeignKey('self',related_name='student_referrer',on_delete=models.SET_NULL,null=True,blank=True)
    photo = models.ImageField(upload_to='employee_document', null=True, blank=True)
    token  = models.TextField(null=True, blank=True)
    is_token_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + "===="+str(self.id)+"========"+str(self.code)
    
class UserProfessionalInfo(BaseModelMixin):

    DAY_CHOICES = [
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
    ]

    CATEGORY_CHOICES = [
        ('weekday', 'Weekdays (Mon–Fri)'),
        ('weekend', 'Weekend (Sat–Sun)'),
        ('custom', 'Custom Days'),
    ]
    user_info=models.ForeignKey(EmployeeCompanyInfo, on_delete=models.CASCADE, blank=True, null=True)
    skills=models.CharField(max_length=220, null=True, blank=True)
    position=models.CharField(max_length=220, null=True, blank=True)
    Description=models.TextField(null=True, blank=True)
    Experience=models.IntegerField(default=0)
    available_days_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    custom_days = MultiSelectField(choices=DAY_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-fill days based on selected category
        if self.available_days_category == "weekday":
            self.custom_days = ['mon', 'tue', 'wed', 'thu', 'fri']
        elif self.available_days_category == "weekend":
            self.custom_days = ['sat', 'sun']
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.available_days_category} - {self.custom_days}"
    rating=models.CharField(max_length=5, null=True, blank=True)
    portfolio_photo = models.ImageField(upload_to='portfolio_photos/', null=True, blank=True)