from django.db import models
from django.contrib.auth.models import User
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now

class UserDesignation(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    is_client = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_contarctor = models.BooleanField(default=False)

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
    
# class EmployeeDocument(BaseModelMixin):

#     title = models.CharField(max_length=220, null=True, blank=True)
#     photo = models.ImageField(upload_to='employee_document', null=True, blank=True)
#     time_stamp = models.DateTimeField(default=now, editable=True)

#     def __str__(self):
#         title = str(self.id)+"==="+str(self.time_stamp) 
#         return title




