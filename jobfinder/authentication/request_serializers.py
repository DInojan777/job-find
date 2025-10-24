from rest_framework import serializers


class RegisterCompanySerializer(serializers.Serializer):
    registered_name = serializers.CharField(required=True)
    brand_name = serializers.CharField(required=True)
    brand_service_type_id = serializers.UUIDField(required=False)
    brand_sector_id = serializers.UUIDField(required=False)
    communication_address = serializers.CharField(required=True)
    pincode = serializers.CharField(required=False)
    provider_company_branch_id = serializers.UUIDField(required=False)
