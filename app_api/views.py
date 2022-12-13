from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
# from app_auth.models import User 


# url: /api/v1/get-user-data/
class GetUserData(APIView):
    def get(self, request):
        data = {
            'is_superuser': request.user.is_superuser,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
        }
        return Response({'data': data, 'status': 200})
