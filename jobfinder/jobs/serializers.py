from rest_framework import serializers
from .models import *

class GetJobListSerilizers(serializers.ModelSerializer):

    class Meta:
        model=Joblist
        fields=['provider_info','description']
