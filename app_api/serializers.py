from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from app_auth.models import User, ManagerModel, DoctorModel, PatientModel
from .models import LabModel, LabResultModel, LabResultCategoryModel, SonographyCenterModel, SonographyResultModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'password', 'is_staff', 'is_active', 'groups', 'user_permissions']


class ManagerSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    permission = serializers.CharField()

    class Meta:
        model = ManagerModel
        fields = '__all__'


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabModel
        fields = '__all__'


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResultModel
        fields = '__all__'


class LabResultRegisterSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField()
    patinet_username = serializers.IntegerField()
    lab_username = serializers.IntegerField()

    class Meta:
        model = LabResultModel
        fields = ['title', 'result', 'category_title', 'patinet_username', 'lab_username']


class SonographyResultRegisterSerializer(serializers.ModelSerializer):
    patinet_username = serializers.IntegerField()
    sono_username = serializers.IntegerField()

    class Meta:
        model = SonographyResultModel
        fields = ['patinet_username', 'sono_username', 'result']


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


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = '__all__'



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientModel
        fields = '__all__'


# class UserPasswordForm(serializers.Serializer):
#     new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
#     new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

#     def validate(self, data):
#         if data['new_password1'] != data['new_password2']:
#             raise serializers.ValidationError({'new_password2': _("باید مقدار دو فیلد برابر باشند.")})
#         return data
