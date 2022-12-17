from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from app_auth.models import PatientModel, User
from rest_framework.permissions import AllowAny
from .serializers import LabResultSerializer, SonographyResultSerializer, UserSerializer
from .models import LabResultModel, SonographyResultModel


# url: /api/v1/get-patient-data/
class GetPatientData(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        code = request.POST.get('code')
        if code:
            if PatientModel.objects.filter(username=code).exists():
                patient = PatientModel.objects.get(username=code)
                lab_res = LabResultModel.objects.filter(patient=patient).all()
                sonography_res = SonographyResultModel.objects.filter(patient=patient).all()
                
                lab_res_serializer = LabResultSerializer(lab_res, many=True)
                sonography_res_serializer  = SonographyResultSerializer(sonography_res, many=True)
                
                response_data =  {
                    'lab_res': lab_res_serializer.data, 
                    'sonography_res': sonography_res_serializer.data, 
                    'status': 200
                }
                return Response(response_data)
            return Response({'status': 400})
        return Response({'status': 400})


# url: /api/v1/get-user-data/
class GetUserData(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        code = request.POST.get('code')
        if code:
            if User.objects.filter(username=code).exists():
                user = User.objects.get(username=code)
                
                user_serializer = UserSerializer(user)
                
                response_data =  {
                    'data': user_serializer.data, 
                    'status': 200
                }
                return Response(response_data)
            return Response({'status': 400})
        return Response({'status': 400})