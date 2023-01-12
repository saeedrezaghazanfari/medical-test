from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        print(attrs)
        # data.update({'is_sono': self.user.sonographycentermodel_set.filter(is_active=True).exists()})
        # data.update({'is_lab': self.user.labmodel_set.filter(is_active=True).exists()})
        # data.update({'is_doctor': self.user.doctormodel_set.filter(is_active=True).exists()})
        # data.update({'is_manager': self.user.managermodel_set.filter(is_active=True).exists()})
        # data.update({'is_admin': self.user.is_superuser})
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer