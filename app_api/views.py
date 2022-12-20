from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from app_auth.models import PatientModel, User, ManagerModel
from rest_framework.permissions import AllowAny
from .serializers import (
    LabResultSerializer, 
    SonographyResultSerializer, 
    SonographyCenterSerializer,
    LabSerializer,
    UserSerializer,
    LabResultCategorySerializer,
    ManagerSerializer
)
from .models import (
    SonographyCenterModel,
    LabModel,
    LabResultCategoryModel,
    LabResultModel, 
    SonographyResultModel
)


# url: /api/v1/get/patient/data/
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


# url: /api/v1/get/user/data/
class GetUserData(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        if request.user:
            user = User.objects.get(username=request.user.username)
            user_serializer = UserSerializer(user)
            
            response_data =  {
                'data': user_serializer.data, 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/sonography-center/
class CreateSonographyCenter(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):
        if request.user:

            serializer = SonographyCenterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            SonographyCenterModel.objects.create(
                title=request.POST.get('title'),
                code=request.POST.get('code'),
                pos=request.POST.get('pos'),
                phone=request.POST.get('phone'),
                permission=request.POST.get('permission'),
            )
            
            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab/
class CreateLab(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):

        if request.user:

            serializer = LabSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            LabModel.objects.create(
                title=request.POST.get('title'),
                code=request.POST.get('code'),
                pos=request.POST.get('pos'),
                phone=request.POST.get('phone'),
                permission=request.POST.get('permission'),
            )
            
            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/lab-category/
class CreateLabCategory(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):

        if request.user:

            serializer = LabResultCategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            LabResultCategoryModel.objects.create(
                title=request.POST.get('title'),
            )
            
            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})


# url: /api/v1/create/manager/
class CreateManager(APIView):

    # permission_classes = [AllowAny] #TODO

    def post(self, request):

        if request.user:

            serializer = ManagerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                permission=request.POST.get('permission'),
            )

            ManagerModel.objects.create(
                user=user
            )
            
            response_data =  { 
                'status': 200
            }
            return Response(response_data)
        return Response({'status': 400})
