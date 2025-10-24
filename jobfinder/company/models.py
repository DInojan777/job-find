from email.policy import default
from django.db import models
from authentication.models import BaseModelMixin
from django.contrib.auth.models import User 
from django.utils.timezone import now

class CompanySector(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name + "==="+str(self.id)

class CompanyTypeOfBusiness(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name + "==="+str(self.id)

class CompanyMeta(BaseModelMixin):
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=30, null=True, blank=True)
    registered_name = models.CharField(max_length=200, null=True, blank=True)
    business_type = models.CharField(max_length=20, null=True, blank=True)
    pan = models.CharField(max_length=30, null=True, blank=True)
    gst = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    sector = models.ForeignKey(
        CompanySector, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_business = models.ForeignKey(
        CompanyTypeOfBusiness, on_delete=models.SET_NULL, null=True, blank=True)
    attachment_gst = models.ImageField(
        upload_to='companymeta', null=True, blank=True)
    attachment_logo = models.ImageField(
        upload_to='companymeta', null=True, blank=True)
    attachment_pan = models.ImageField(
        upload_to='companymeta', null=True, blank=True)
    details = models.CharField(max_length=220, null=True, blank=True)
    type_is_provider = models.BooleanField(default=False)
    # digital_profile=models.JSONField(default=[{"profile":"linkedin","is_manditory":True,"is_required":True},
    # {"profile":"facebook","is_manditory":True,"is_required":True},
    # {"profile":"instagram","is_manditory":True,"is_required":True}],null=True,blank=True)
    employee_size = models.CharField(max_length=30, null=True, blank=True)
    created_by_company = models.ForeignKey('self', on_delete=models.SET_NULL, related_name = 'created_company',null=True, blank=True)

    def __str__(self):
        return self.brand_name + "==="+str(self.id)

class CompanyContactInfo(BaseModelMixin):
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


class CompanyBranchInfo(BaseModelMixin):
    company = models.ForeignKey(
        CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    provider_company_branch = models.ForeignKey('self', related_name='admin_company_branch', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    branch_id = models.CharField(max_length=30, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    branch_code = models.CharField(max_length=10, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    can_update_location = models.BooleanField(default=False)
    company_contact = models.ForeignKey(CompanyContactInfo, unique=True, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        title = str(self.name) + "===" + \
            str(self.is_parent) + "==="+str(self.id)+"====="+str(self.code)
        if self.parent is not None:
            title = title + "===" + str(self.parent.id)+"====="+str(self.code)
        return title

class WeekDay(BaseModelMixin):
    is_working = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

class CompanyDepartment(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    company = models.ForeignKey(
        CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(
        CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + "==="+str(self.id)+"====="+str(self.code)