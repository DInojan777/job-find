from django.db import models
from django.contrib.auth.models import User  # new
import uuid
import random
import string

class BaseModelMixin(models.Model):

    created_message = "Details created successfully"
    updated_message = "Details Updated Successfully"
    unique_fail_message = "Record with provided details already exist"


    unique_fields = []
    unique_group = []
    foreign_fields = []

    def get_foreign_field_class(self, name):
        return None

    many_to_many_fields = ['tags']

    def get_many_to_many_class(self, name):
        return None
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    code=models.CharField(max_length=210,null=True,blank=True)
    custom_field=models.JSONField(default=dict, null=True, blank=True)

    def get_custom_field(self, key, fbv = None):
        try:
            return self.custom_fields[key]
        except:
            return fbv
 
    def add_custom_field(self, key, value):
        
        custom_fields = self.custom_fields
        custom_fields[key] = value
        self.custom_fields = custom_fields
        self.save()
 
    def add_custom_fields(self, obj):    
        custom_fields = self.custom_fields
        for key in obj.keys():        
            custom_fields[key] = obj[key]
        self.custom_fields = custom_fields
        self.save()      

    class Meta:
        abstract = True
        ordering = ['-created_at']

class AppBaseConfig(BaseModelMixin):
    current_version_android = models.CharField(
        max_length=8, null=True, blank=True)
    minimum_support_version_android = models.CharField(
        max_length=8, null=True, blank=True)
    current_version_ios = models.CharField(max_length=8, null=True, blank=True)
    minimum_support_version_ios = models.CharField(
        max_length=8, null=True, blank=True)
    last_sync_time = models.DateTimeField(
        auto_now=False, null=True, blank=True)
    cron_start_time = models.DateTimeField(
        auto_now=False, null=True, blank=True)
    cron_end_time = models.DateTimeField(
        auto_now=False, null=True, blank=True)
    bypass_password = models.CharField(default="Leora@2024",
        max_length=210, null=True, blank=True)

class UserAuthentication(BaseModelMixin):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    mobile_otp = models.CharField(max_length=8, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)
    is_job_seeker= models.BooleanField(default=True)
    is_super_admin = models.BooleanField(default=False)
    is_guest=models.BooleanField(default=False)
    is_login_action = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    last_active_time = models.DateTimeField(null=True, blank=True)
    user_registation_status = models.IntegerField(default=0)
    admin_registration_designation = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class UserCredentialValidation(BaseModelMixin):
    mobile_number = models.CharField(max_length=12, null=True, blank=True)
    mobile_otp = models.CharField(max_length=8, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    user_registation_status = models.IntegerField(default=0)
    admin_registration_designation = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return self.mobile_number
