from django.contrib import admin
from .models import *

admin.site.register(UserAuthentication)
admin.site.register(UserCredentialValidation)
admin.site.register(AppBaseConfig)


