from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from .models import LabModel, LabResultModel, LabResultCategoryModel, SonographyCenterModel, SonographyResultModel
    
# class BankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankModel
#         exclude = ['user']


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabModel
        fields = '__all__'


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResultModel
        fields = '__all__'


class LabResultCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResultCategoryModel
        fields = '__all__'


class SonographyCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SonographyCenterModel
        fields = '__all__'


class SonographyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SonographyResultModel
        fields = '__all__'

